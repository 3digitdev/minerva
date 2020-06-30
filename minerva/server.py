from flask import Flask, request, jsonify, make_response
from connectors.mongo import MongoConnector
from helpers.helpers import verify_request_body, BadRequestError

from categories.notes import Note

URL_BASE = "/api/v1"

app = Flask(__name__)


@app.route(f"{URL_BASE}/notes", methods=["GET", "POST"])
def all_notes():
    with MongoConnector() as mongo:
        if request.method == "GET":
            return make_response({"notes": mongo.find_all_notes()}, 200)
        elif request.method == "POST":
            try:
                verify_request_body(request.json, Note.required())
            except BadRequestError as e:
                return make_response({"error": e.msg}, 400)
            note = Note.from_request(request.json)
            note_id = mongo.create_note(note)
            return make_response({"id": note_id}, 201)


@app.route(f"{URL_BASE}/notes/<string:note_id>", methods=["GET", "PUT", "DELETE"])
def note_by_id(note_id: str):
    with MongoConnector() as mongo:
        if request.method == "GET":
            note = mongo.find_single_note(note_id)
            if note:
                parsed_note = Note(
                    id=str(note["_id"]), contents=note["contents"], url=note["url"]
                )
                return make_response(parsed_note.__dict__(), 200)
            return make_response(
                {"error": f"Could not find a Note with the ID '{note_id}'"}, 404
            )
        elif request.method == "PUT":
            updated_note = Note.from_request(request.json)
            result = mongo.update_note(note_id, updated_note)
            if result:
                return make_response(result, 200)
            return make_response(
                {"error": f"Could not find a Note with the ID '{note_id}'"}, 404
            )
        elif request.method == "DELETE":
            if mongo.delete_note(note_id) > 0:
                return make_response({}, 204)
            return make_response(
                {"error": f"Could not find a Note with the ID '{note_id}'"}, 404
            )
