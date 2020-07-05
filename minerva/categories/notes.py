from typing import List

import attr

from .category import Category
from ..helpers.types import JsonData
from ..helpers.validators import validate_tag_list


@attr.s
class Note(Category):
    contents: str = attr.ib()
    url: str = attr.ib(default="")
    # ---
    tags: List[str] = attr.ib(default=[], validator=validate_tag_list)
    id: str = attr.ib(default="")

    def __dict__(self) -> JsonData:
        return {"_id": self.id, "contents": self.contents, "url": self.url, "tags": self.tags}

    def to_json(self) -> JsonData:
        return {"contents": self.contents, "url": self.url, "tags": self.tags}

    @staticmethod
    def from_request(req: JsonData) -> "Note":
        Note.verify_request_body(req)
        return Note(contents=req["contents"], url=req.get("url", ""), tags=req.get("tags", []))

    @staticmethod
    def verify_request_body(body: JsonData) -> None:
        Category.verify_incoming_request(
            body=body, required_fields=["contents"], optional_fields=["url", "tags"], category=Note
        )

    @staticmethod
    def collection() -> str:
        return "notes"
