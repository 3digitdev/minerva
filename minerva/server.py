from typing import Type

from flask import Flask, request, make_response, Response

from categories.category import Category
from categories.dates import Date
from categories.links import Link
from categories.logins import Login
from categories.tags import Tag
from connectors.mongo import MongoConnector
from categories.notes import Note
from helpers.exceptions import HttpError


class Route:
    def __init__(self, cat: Type[Category]):
        self.single: str = str(cat.__name__.lower())
        self.multi: str = self.single + "s"
        self.category: Type[Category] = cat

    @classmethod
    def build(cls, cat: Type[Category]) -> "Route":
        return cls(cat)

    def item_not_found(self, item_id: str) -> Response:
        return make_response(
            {"error": f"Could not find a {str(self.category.__name__)} with the ID '{item_id}'"},
            404,
        )

    def all_items(self):
        try:
            with MongoConnector(self.category) as db:
                if request.method == "GET":
                    found_items = db.find_all()
                    return make_response({self.multi: [i.__dict__() for i in found_items]}, 200)
                elif request.method == "POST":
                    self.category.verify_request_body(request.json)
                    item = self.category.from_request(request.json)
                    item_id = db.create(item)
                    return make_response({"id": item_id}, 201)
        except HttpError as e:
            return make_response({"error": e.msg}, e.code)

    def item_by_id(self, item_id: str):
        try:
            with MongoConnector(self.category) as db:
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


URL_BASE = "/api/v1"

app = Flask(__name__)


# region TAG ROUTES
@app.route(f"{URL_BASE}/tags", methods=["GET", "POST"])
def all_tags():
    return Route.build(Tag).all_items()


@app.route(f"{URL_BASE}/tags/<string:tag_id>", methods=["GET", "PUT", "DELETE"])
def tag_by_id(tag_id: str):
    return Route.build(Tag).item_by_id(item_id=tag_id)


# endregion


# region NOTE ROUTES
@app.route(f"{URL_BASE}/notes", methods=["GET", "POST"])
def all_notes():
    return Route.build(Note).all_items()


@app.route(f"{URL_BASE}/notes/<string:note_id>", methods=["GET", "PUT", "DELETE"])
def note_by_id(note_id: str):
    return Route.build(Note).item_by_id(item_id=note_id)


# endregion


# region LOGIN ROUTES
@app.route(f"{URL_BASE}/logins", methods=["GET", "POST"])
def all_login():
    return Route.build(Login).all_items()


@app.route(f"{URL_BASE}/logins/<string:login_id>", methods=["GET", "PUT", "DELETE"])
def login_by_id(login_id: str):
    return Route.build(Login).item_by_id(item_id=login_id)


# endregion


# region DATE ROUTES
@app.route(f"{URL_BASE}/dates", methods=["GET", "POST"])
def all_dates():
    return Route.build(Date).all_items()


@app.route(f"{URL_BASE}/dates/<string:date_id>", methods=["GET", "PUT", "DELETE"])
def date_by_id(date_id: str):
    return Route.build(Date).item_by_id(item_id=date_id)


# endregion


# region LINK ROUTES
@app.route(f"{URL_BASE}/links", methods=["GET", "POST"])
def all_links():
    return Route.build(Link).all_items()


@app.route(f"{URL_BASE}/links/<string:link_id>", methods=["GET", "PUT", "DELETE"])
def link_by_id(link_id: str):
    return Route.build(Link).item_by_id(item_id=link_id)


# endregion
