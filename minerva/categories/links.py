from typing import List

import attr

from .category import Category
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
        return {
            "_id": self.id,
            "name": self.name,
            "url": self.url,
            "notes": self.notes,
            "tags": self.tags,
        }

    def to_json(self) -> JsonData:
        return {"name": self.name, "url": self.url, "notes": self.notes, "tags": self.tags}

    @staticmethod
    def from_request(req: JsonData) -> "Link":
        Link.verify_request_body(req)
        return Link(
            name=req["name"], url=req["url"], notes=req.get("notes", []), tags=req.get("tags", [])
        )

    @staticmethod
    def verify_request_body(body: JsonData) -> None:
        Category.verify_incoming_request(
            body=body,
            required_fields=["name", "url"],
            optional_fields=["notes", "tags"],
            category=Link,
        )

    @staticmethod
    def collection() -> str:
        return "links"
