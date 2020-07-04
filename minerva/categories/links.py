from typing import List

import attr

from .category import Category
from ..helpers.exceptions import BadRequestError
from ..helpers.types import JsonData
from ..helpers.validators import validate_tag_list


@attr.s
class Link(Category):
    name: str = attr.ib()
    url: str = attr.ib()
    notes: List[str] = attr.ib(default=[])
    # ---
    tags: List[str] = attr.ib(default=[], validator=validate_tag_list)
    id: str = attr.ib(default="")

    def __dict__(self) -> JsonData:
        return {"_id": self.id, "url": self.url, "notes": self.notes, "tags": self.tags}

    def to_json(self) -> JsonData:
        return {"url": self.url, "notes": self.notes, "tags": self.tags}

    @staticmethod
    def from_request(req: JsonData) -> "Link":
        Link.verify_request_body(req)
        return Link(
            name=req["name"], url=req["url"], notes=req.get("notes", []), tags=req.get("tags", [])
        )

    @staticmethod
    def verify_request_body(body: JsonData) -> None:
        required = ["name", "url"]
        for field in required:
            if field not in body:
                raise BadRequestError(f"Invalid request -- missing field '{field}' in Link")

    @staticmethod
    def collection() -> str:
        return "links"
