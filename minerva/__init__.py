import os
from typing import Type

from flask import Flask, request, make_response, Response

from .categories.category import Category
from .categories.dates import Date
from .categories.employments import Employment
from .categories.housings import Housing
from .categories.links import Link
from .categories.logins import Login
from .categories.recipes import Recipe
from .categories.tags import Tag
from .connectors.mongo import MongoConnector
from .categories.notes import Note
from .helpers.exceptions import HttpError, BadRequestError

URL_BASE = "/api/v1"
TESTING = False


class Route:
    def __init__(self, cat: Type[Category], is_test: bool):
        self.single: str = str(cat.__name__.lower())
        self.multi: str = self.single + "s"
        self.category: Type[Category] = cat
        self.is_test = is_test

    @classmethod
    def build(cls, cat: Type[Category], is_test: bool) -> "Route":
        return cls(cat, is_test)

    def item_not_found(self, item_id: str) -> Response:
        return make_response(
            {"error": f"Could not find a {str(self.category.__name__)} with the ID '{item_id}'"},
            404,
        )

    def all_items(self):
        try:
            with MongoConnector(self.category, is_test=self.is_test) as db:
                if request.method == "GET":
                    found_items = db.find_all()
                    return make_response({self.multi: [i.__dict__() for i in found_items]}, 200)
                elif request.method == "POST":
                    if not request.json:
                        raise BadRequestError("Expected a json body but received none")
                    self.category.verify_request_body(request.json)
                    item = self.category.from_request(request.json)
                    item_id = db.create(item)
                    return make_response({"id": item_id}, 201)
        except HttpError as e:
            return make_response({"error": e.msg}, e.code)

    def item_by_id(self, item_id: str):
        try:
            with MongoConnector(self.category, is_test=self.is_test) as db:
                if request.method == "GET":
                    item = db.find_one(item_id)
                    if item:
                        return make_response(item.__dict__(), 200)
                    return self.item_not_found(item_id)
                elif request.method == "PUT":
                    if not db.find_one(item_id):
                        return self.item_not_found(item_id)
                    updated_item = self.category.from_request(request.json)
                    result = db.update_one(item_id, updated_item)
                    if result:
                        return make_response(result.__dict__(), 200)
                    return self.item_not_found(item_id)
                elif request.method == "DELETE":
                    if db.delete_one(item_id) > 0:
                        return make_response({}, 204)
                    return self.item_not_found(item_id)
        except HttpError as e:
            return make_response({"error": e.msg}, e.code)


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    is_test = (test_config or {}).get("TESTING", False)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # region TAG ROUTES
    @app.route(f"{URL_BASE}/tags", methods=["GET", "POST"])
    def all_tags():
        return Route.build(Tag, is_test).all_items()

    @app.route(f"{URL_BASE}/tags/<string:tag_id>", methods=["GET", "PUT", "DELETE"])
    def tag_by_id(tag_id: str):
        return Route.build(Tag, is_test).item_by_id(item_id=tag_id)

    # endregion

    # region NOTE ROUTES
    @app.route(f"{URL_BASE}/notes", methods=["GET", "POST"])
    def all_notes():
        return Route.build(Note, is_test).all_items()

    @app.route(f"{URL_BASE}/notes/<string:note_id>", methods=["GET", "PUT", "DELETE"])
    def note_by_id(note_id: str):
        return Route.build(Note, is_test).item_by_id(item_id=note_id)

    # endregion

    # region LOGIN ROUTES
    @app.route(f"{URL_BASE}/logins", methods=["GET", "POST"])
    def all_login():
        return Route.build(Login, is_test).all_items()

    @app.route(f"{URL_BASE}/logins/<string:login_id>", methods=["GET", "PUT", "DELETE"])
    def login_by_id(login_id: str):
        return Route.build(Login, is_test).item_by_id(item_id=login_id)

    # endregion

    # region DATE ROUTES
    @app.route(f"{URL_BASE}/dates", methods=["GET", "POST"])
    def all_dates():
        return Route.build(Date, is_test).all_items()

    @app.route(f"{URL_BASE}/dates/<string:date_id>", methods=["GET", "PUT", "DELETE"])
    def date_by_id(date_id: str):
        return Route.build(Date, is_test).item_by_id(item_id=date_id)

    # endregion

    # region LINK ROUTES
    @app.route(f"{URL_BASE}/links", methods=["GET", "POST"])
    def all_links():
        return Route.build(Link, is_test).all_items()

    @app.route(f"{URL_BASE}/links/<string:link_id>", methods=["GET", "PUT", "DELETE"])
    def link_by_id(link_id: str):
        return Route.build(Link, is_test).item_by_id(item_id=link_id)

    # endregion

    # region HOUSING HISTORY ROUTES
    @app.route(f"{URL_BASE}/housing", methods=["GET", "POST"])
    def all_housing():
        return Route.build(Housing, is_test).all_items()

    @app.route(f"{URL_BASE}/housing/<string:house_id>", methods=["GET", "PUT", "DELETE"])
    def house_by_id(house_id: str):
        return Route.build(Housing, is_test).item_by_id(item_id=house_id)

    # endregion

    # region EMPLOYMENT HISTORY ROUTES
    @app.route(f"{URL_BASE}/employment", methods=["GET", "POST"])
    def all_employment():
        return Route.build(Employment, is_test).all_items()

    @app.route(f"{URL_BASE}/employment/<string:job_id>", methods=["GET", "PUT", "DELETE"])
    def employment_by_id(job_id: str):
        return Route.build(Employment, is_test).item_by_id(item_id=job_id)

    # endregion

    # region RECIPE ROUTES
    @app.route(f"{URL_BASE}/recipes", methods=["GET", "POST"])
    def all_recipes():
        return Route.build(Recipe, is_test).all_items()

    @app.route(f"{URL_BASE}/recipes/<string:recipe_id>", methods=["GET", "PUT", "DELETE"])
    def recipe_by_id(recipe_id: str):
        return Route.build(Recipe, is_test).item_by_id(item_id=recipe_id)

    # endregion

    return app
