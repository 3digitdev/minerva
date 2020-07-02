from typing import Type

from flask import Flask, request, make_response, Response

from categories.category import Category
from categories.logins import Login
from categories.tags import Tag
from connectors.mongo import MongoConnector
from categories.notes import Note
from helpers.exceptions import BadRequestError


class Route:
    def __init__(self, cat: Type[Category]):
        self.single: str = str(cat.__name__.lower())
        self.multi: str = self.single + "s"
        self.category: Type[Category] = cat


URL_BASE = "/api/v1"

app = Flask(__name__)


def not_found(route: Route, item_id: str) -> Response:
    return make_response(
        {
            "error": f"Could not find a {str(route.category.__name__)} with the ID '{item_id}'"
        },
        404,
    )


def all_items(route: Route):
    with MongoConnector(route.category) as db:
        if request.method == "GET":
            return make_response({route.multi: db.find_all()}, 200)
        elif request.method == "POST":
            try:
                route.category.verify_request_body(request.json)
            except BadRequestError as e:
                return make_response({"error": e.msg}, 400)
            item = route.category.from_request(request.json)
            item_id = db.create(item)
            return make_response({"id": item_id}, 201)


def item_by_id(route: Route, item_id: str):
    with MongoConnector(route.category) as db:
        if request.method == "GET":
            item = db.find_one(item_id)
            if item:
                return make_response(route.category.from_mongo(item).__dict__(), 200)
            return not_found(route, item_id)
        elif request.method == "PUT":
            if not db.find_one(item_id):
                return not_found(route, item_id)
            updated_item = route.category.from_request(request.json)
            result = db.update_one(item_id, updated_item)
            if result:
                return make_response(result, 200)
            return not_found(route, item_id)
        elif request.method == "DELETE":
            if db.delete_one(item_id) > 0:
                return make_response({}, 204)
            return not_found(route, item_id)


# region TAG ROUTES
@app.route(f"{URL_BASE}/tags", methods=["GET", "POST"])
def all_tags():
    return all_items(route=Route(Tag))


@app.route(f"{URL_BASE}/tags/<string:tag_id>", methods=["GET", "PUT", "DELETE"])
def tag_by_id(tag_id: str):
    return item_by_id(route=Route(Tag), item_id=tag_id)


# endregion


# region NOTE ROUTES
@app.route(f"{URL_BASE}/notes", methods=["GET", "POST"])
def all_notes():
    return all_items(route=Route(Note))


@app.route(f"{URL_BASE}/notes/<string:note_id>", methods=["GET", "PUT", "DELETE"])
def note_by_id(note_id: str):
    return item_by_id(route=Route(Note), item_id=note_id)


# endregion


# region LOGIN ROUTES
@app.route(f"{URL_BASE}/logins", methods=["GET", "POST"])
def all_login():
    return all_items(route=Route(Login))


@app.route(f"{URL_BASE}/logins/<string:login_id>", methods=["GET", "PUT", "DELETE"])
def login_by_id(login_id: str):
    return item_by_id(route=Route(Login), item_id=login_id)


# endregion
