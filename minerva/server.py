from flask import Flask, request

URL_BASE = "/api/v1"

app = Flask(__name__)


@app.route(f"{URL_BASE}/notes", methods=["GET", "POST"])
def all_notes():
    if request.method == "GET":
        return "TODO: GET ALL NOTES"
    elif request.method == "POST":
        return "TODO: CREATE NOTE"


@app.route(f"{URL_BASE}/notes/<int:note_id>", methods=["GET", "PUT"])
def note_by_id(note_id: int):
    if request.method == "GET":
        return "TODO: GET NOTE BY ID"
    elif request.method == "PUT":
        return "TODO: UPDATE NOTE"
