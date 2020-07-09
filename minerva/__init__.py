import os
import attr

from typing import Type, List, Callable
from flask import Flask, request, make_response, Response
from pymongo.errors import DuplicateKeyError

from .categories.category import Category
from .categories.logs import Log
from .categories.api_keys import ApiKey
from .categories.dates import Date
from .categories.employments import Employment
from .categories.housings import Housing
from .categories.links import Link
from .categories.logins import Login
from .categories.recipes import Recipe
from .categories.tags import Tag
from .connectors.base_connector import BaseConnector
from .connectors.datastore_factory import DatastoreFactory
from .categories.notes import Note
from .helpers.exceptions import HttpError, BadRequestError, NotFoundError, InternalServerError
from .helpers.custom_types import Maybe, JsonData
from .helpers.authorization import validate_key
from .helpers.logging import Logger
from .helpers.config_loader import load_config

URL_BASE = "/api/v1"
# Note that not all Category subtypes are here.  This is only the Category subtypes
# that will have API endpoints created for them!
ALL_TYPES = [Date, Employment, Housing, Link, Login, Note, Recipe, Tag]


@attr.s
class Hooks:
    """
    This is used as a helper for the Route object to allow certain methods to
    be given that run at certain times.  This is almost CERTAINLY a code smell
    on my part.  See the Route for notes on my thoughts for that.
    """

    # Used for cascading tags deletion
    after_delete: Callable[[Category], None] = attr.ib(default=lambda x: None)
    # Used for cascading tags updates
    after_update: Callable[[Category, Category], None] = attr.ib(default=lambda x, y: None)


class Route:
    """
    TODO:  Re-evaluate the Route object and see if its worth it to abstract that much.
    This thing is a bit weird, but it handles a ton of boilerplate for super-basic
    CRUD endpoint creation for any given Category object.
    """

    def __init__(self, cat: Type[Category], config: JsonData, hooks: Maybe[JsonData] = None):
        self.hooks: JsonData = hooks or {}
        self.config: JsonData = config
        self.single: str = str(cat.__name__.lower())  # Object name as a string ("Date" -> "date")
        self.multi: str = self.single + "s"  # used for endpoint path building
        self.category: Type[Category] = cat
        # Delineates whether we are running the Flask API in "testing" mode
        self.is_test: bool = config.get("TESTING", False)
        # Unit tests don't need an API key
        self.api_key: Maybe[ApiKey] = (ApiKey("", "TEST_USER") if self.is_test else None)
        # Create the preferred DB Connector
        self.datastore: Type[BaseConnector] = DatastoreFactory.build(self.config)
        # Logger object
        self.logger = Logger(self.datastore, self.config)

        try:
            self.hooks = Hooks(**hooks)
        except Exception as e:
            raise InternalServerError(f"Invalid hooks: {str(e)}")

    @classmethod
    def build(cls, cat: Type[Category], config: JsonData, hooks: Maybe[JsonData] = None) -> "Route":
        """
        This is a builder-pattern-like method to allow for some method chaining down below
        :param cat: The type of Category being built
        :param config: The application config data
        :param hooks: Any hooks to apply
        :return: The new Route object (for method chaining)
        """
        hooks = hooks or {}
        return cls(cat, config, hooks)

    def item_not_found(self, item_id: str) -> Response:
        """
        Helper function to reduce magic string repetition for a common error type
        :param item_id: The ID that didn't match the datastore entries
        :return: A Flask Response object
        """
        return make_response(
            {"error": f"Could not find a {str(self.category.__name__)} with the ID '{item_id}'"},
            404,
        )

    @staticmethod
    def log_http_error(logger: Logger, api_key: Maybe[ApiKey], e: HttpError) -> None:
        """
        Logging helper function for any given error that gets thrown
        :param logger: The Logger object
        :param api_key: The API key for the user that called the endpoint that errored out
        :param e: The error object to be logged
        :return: N/A
        """
        logger.error(
            request,
            user=api_key.user if api_key else "UNKNOWN_USER",
            message=f"[{e.code}] {e.msg}",
            details={"error": e.__class__.__name__},
        )

    def all_items(self) -> Response:
        """
        A function that manages the "all" endpoints -- /objects
        GET:  Get the (possibly paginated) list of objects of a given type
        POST:  Create a new instance of an object of a given type
        :return: The Flask Response object after the endpoint is called
        """
        try:
            if not self.is_test:
                self.api_key: ApiKey = validate_key(
                    request.headers.get("x-api-key", None), self.datastore, self.config
                )
            with self.datastore(self.category, config=self.config) as db:
                if request.method == "GET":
                    try:
                        page_num = int(request.args.get("page", 1))
                        num_per_page = int(request.args.get("count", 10))
                    except ValueError:
                        raise BadRequestError("'page' and 'count' must be integers if provided")
                    no_limit = request.args.get("all", None)
                    if no_limit:
                        found_items = db.find_all_no_limit()
                    else:
                        found_items = db.find_all(page=page_num, count=num_per_page)
                    resp_body = {self.multi: [i.__dict__() for i in found_items]}
                    self.logger.info(
                        request,
                        user=self.api_key.user if self.api_key else "TEST_USER",
                        message=f"Found {len(found_items)} items",
                        details=resp_body,
                    )
                    return make_response(resp_body, 200)
                elif request.method == "POST":
                    if not request.json:
                        raise BadRequestError("Expected a json body but received none")
                    self.category.verify_request_body(request.json)
                    item = self.category.from_request(request.json)
                    try:
                        item_id = db.create(item)
                    except DuplicateKeyError as e:
                        raise BadRequestError(str(e))
                    self.logger.info(
                        request,
                        user=self.api_key.user if self.api_key else "TEST_USER",
                        message=f"Created {item_id}",
                    )
                    return make_response({"id": item_id}, 201)
        except HttpError as e:
            Route.log_http_error(self.logger, self.api_key, e)
            return make_response({"error": e.msg}, e.code)

    def item_by_id(self, item_id: str) -> Response:
        """
        A function that manages the "by ID" endpoints -- /objects/<object_od>
        GET:  Get a single object of a given type by ID
        PUT:  Update a single object of a given type by ID with values
        DELETE:  Delete a single object of a given type by ID
        :param item_id: The unique ID of the object to handle
        :return: The Flask Response object after the endpoint is called
        """
        try:
            if not self.is_test:
                self.api_key: ApiKey = validate_key(
                    request.headers.get("x-api-key", None), self.datastore, self.config
                )
            with self.datastore(self.category, config=self.config) as db:
                if request.method == "GET":
                    item = db.find_one(item_id)
                    if item:
                        self.logger.info(
                            request,
                            user=self.api_key.user if self.api_key else "TEST_USER",
                            message=f"Found {item_id}",
                            details=item.__dict__(),
                        )
                        return make_response(item.__dict__(), 200)
                    return self.item_not_found(item_id)
                elif request.method == "PUT":
                    old_item = db.find_one(item_id)
                    if not old_item:
                        return self.item_not_found(item_id)
                    updated_item = self.category.from_request(request.json)
                    try:
                        result = db.update_one(item_id, updated_item)
                    except DuplicateKeyError as e:
                        raise BadRequestError(str(e))
                    if result:
                        self.hooks.after_update(old_item, updated_item)
                        self.logger.info(
                            request,
                            user=self.api_key.user if self.api_key else "TEST_USER",
                            message=f"Updated {item_id}",
                            details={"old": old_item.__dict__(), "new": result.__dict__()},
                        )
                        return make_response(result.__dict__(), 200)
                    return self.item_not_found(item_id)
                elif request.method == "DELETE":
                    item = db.find_one(item_id)
                    if db.delete_one(item_id) > 0:
                        if item:
                            self.hooks.after_delete(item)
                        self.logger.info(
                            request,
                            user=self.api_key.user if self.api_key else "TEST_USER",
                            message=f"Deleted {item_id}",
                            details={"deleted": item.__dict__()},
                        )
                        return make_response({}, 204)
                    return self.item_not_found(item_id)
        except HttpError as e:
            Route.log_http_error(self.logger, self.api_key, e)
            return make_response({"error": e.msg}, e.code)


def create_app(test_config=None):
    """
    Standard wrapper function for building the Flask API
    :param test_config: A test config as defined by Flask
    :return: The Flask App object
    """
    app = Flask(__name__)
    minerva_config = test_config or {}
    minerva_config.update(load_config())
    is_test = minerva_config.get("TESTING", False)
    datastore: Type[BaseConnector] = DatastoreFactory.build(minerva_config)
    logger: Logger = Logger(datastore, minerva_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # region TAG ROUTES
    @app.route(f"{URL_BASE}/tags", methods=["GET", "POST"])
    def all_tags():
        return Route.build(Tag, minerva_config).all_items()

    def cascade_delete_tag(tag: Tag):
        for item_type in [t for t in ALL_TYPES if t != Tag]:
            with datastore(item_type, minerva_config) as db:
                db.cascade_tag_delete(tag.name)

    def cascade_update_tag(old_tag: Tag, new_tag: Tag):
        for item_type in [t for t in ALL_TYPES if t != Tag]:
            with datastore(item_type, minerva_config) as db:
                db.cascade_tag_update(old_tag.name, new_tag.name)

    @app.route(f"{URL_BASE}/tags/<string:tag_id>", methods=["GET", "PUT", "DELETE"])
    def tag_by_id(tag_id: str):
        return Route.build(
            Tag,
            minerva_config,
            hooks={"after_delete": cascade_delete_tag, "after_update": cascade_update_tag},
        ).item_by_id(item_id=tag_id)

    # endregion

    # region NOTE ROUTES
    @app.route(f"{URL_BASE}/notes", methods=["GET", "POST"])
    def all_notes():
        return Route.build(Note, minerva_config).all_items()

    @app.route(f"{URL_BASE}/notes/<string:note_id>", methods=["GET", "PUT", "DELETE"])
    def note_by_id(note_id: str):
        return Route.build(Note, minerva_config).item_by_id(item_id=note_id)

    # endregion

    # region LOGIN ROUTES
    @app.route(f"{URL_BASE}/logins", methods=["GET", "POST"])
    def all_login():
        return Route.build(Login, minerva_config).all_items()

    @app.route(f"{URL_BASE}/logins/<string:login_id>", methods=["GET", "PUT", "DELETE"])
    def login_by_id(login_id: str):
        return Route.build(Login, minerva_config).item_by_id(item_id=login_id)

    # endregion

    # region DATE ROUTES
    @app.route(f"{URL_BASE}/dates", methods=["GET", "POST"])
    def all_dates():
        return Route.build(Date, minerva_config).all_items()

    # This must be before "by id" to avoid path conflicts!
    @app.route(f"{URL_BASE}/dates/today", methods=["GET"])
    def get_today_events():
        api_key: Maybe[ApiKey] = None
        try:
            if not is_test:
                api_key = validate_key(
                    request.headers.get("x-api-key", None), datastore, minerva_config
                )
            if request.method == "GET":
                with datastore(Date, minerva_config) as db:
                    dates: Maybe[List[Date]] = db.get_today_events()
                    if not dates:
                        raise NotFoundError("No events in the database occur today")
                    resp_body = {"dates": [d.__dict__() for d in dates]}
                    logger.info(
                        request,
                        user=api_key.user if api_key else "TEST_USER",
                        message=f"Found {len(dates)} events",
                        details=resp_body,
                    )
                    return make_response(resp_body, 200)
        except HttpError as e:
            Route.log_http_error(logger, api_key, e)
            return make_response({"error": e.msg}, e.code)

    @app.route(f"{URL_BASE}/dates/<string:date_id>", methods=["GET", "PUT", "DELETE"])
    def date_by_id(date_id: str):
        return Route.build(Date, minerva_config).item_by_id(item_id=date_id)

    # endregion

    # region LINK ROUTES
    @app.route(f"{URL_BASE}/links", methods=["GET", "POST"])
    def all_links():
        return Route.build(Link, minerva_config).all_items()

    @app.route(f"{URL_BASE}/links/<string:link_id>", methods=["GET", "PUT", "DELETE"])
    def link_by_id(link_id: str):
        return Route.build(Link, minerva_config).item_by_id(item_id=link_id)

    # endregion

    # region HOUSING HISTORY ROUTES
    @app.route(f"{URL_BASE}/housings", methods=["GET", "POST"])
    def all_housing():
        return Route.build(Housing, minerva_config).all_items()

    @app.route(f"{URL_BASE}/housings/<string:house_id>", methods=["GET", "PUT", "DELETE"])
    def house_by_id(house_id: str):
        return Route.build(Housing, minerva_config).item_by_id(item_id=house_id)

    # endregion

    # region EMPLOYMENT HISTORY ROUTES
    @app.route(f"{URL_BASE}/employments", methods=["GET", "POST"])
    def all_employment():
        return Route.build(Employment, minerva_config).all_items()

    @app.route(f"{URL_BASE}/employments/<string:job_id>", methods=["GET", "PUT", "DELETE"])
    def employment_by_id(job_id: str):
        return Route.build(Employment, minerva_config).item_by_id(item_id=job_id)

    # endregion

    # region RECIPE ROUTES
    @app.route(f"{URL_BASE}/recipes", methods=["GET", "POST"])
    def all_recipes():
        return Route.build(Recipe, minerva_config).all_items()

    @app.route(f"{URL_BASE}/recipes/<string:recipe_id>", methods=["GET", "PUT", "DELETE"])
    def recipe_by_id(recipe_id: str):
        return Route.build(Recipe, minerva_config).item_by_id(item_id=recipe_id)

    # endregion

    # region LOG ROUTES
    @app.route(f"{URL_BASE}/logs", methods=["GET"])
    def get_logs():
        if request.method == "GET":
            api_key: Maybe[ApiKey] = None
            if not is_test:
                api_key = validate_key(
                    request.headers.get("x-api-key", None), datastore, minerva_config
                )
            with datastore(Log, minerva_config) as db:
                # TODO:  Pagination and filtering query params
                logs: List[Log] = db.get_logs()
                logger.info(
                    request,
                    user=api_key.user if api_key else "TEST_USER",
                    message=f"Found {len(logs)} logs",
                )
                return make_response({"logs": logs}, 200)

    # endregion

    return app
