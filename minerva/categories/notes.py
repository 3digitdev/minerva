import attr

from categories.category import Category
from helpers.exceptions import BadRequestError
from helpers.helpers import JsonData


@attr.s
class Note(Category):
    contents: str = attr.ib()
    url: str = attr.ib(default="")
    id: str = attr.ib(default="")

    def __dict__(self) -> JsonData:
        return {"_id": self.id, "contents": self.contents, "url": self.url}

    def to_json(self) -> JsonData:
        return {"contents": self.contents, "url": self.url}

    @staticmethod
    def from_request(req: JsonData) -> "Note":
        note = Note(contents=req["contents"])
        if "url" in req:
            note.url = req["url"]
        return note

    @staticmethod
    def verify_request_body(body: JsonData) -> None:
        required = ["contents"]
        for field in required:
            if field not in body:
                raise BadRequestError(f"Invalid request -- missing field '{field}' in Note")

    @staticmethod
    def collection() -> str:
        return "notes"
