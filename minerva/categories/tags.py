import attr

from .category import Category
from ..helpers.custom_types import JsonData


@attr.s
class Tag(Category):
    name: str = attr.ib()
    id: str = attr.ib(default="")

    def __dict__(self) -> JsonData:
        return {"_id": self.id, "name": self.name}

    def to_json(self) -> JsonData:
        return {"name": self.name}

    @staticmethod
    def from_request(req: JsonData) -> "Tag":
        Tag.verify_request_body(req)
        return Tag(name=req["name"])

    @staticmethod
    def verify_request_body(body: JsonData) -> None:
        Category.verify_incoming_request(
            body=body, required_fields=["name"], optional_fields=[], category=Tag
        )

    @staticmethod
    def collection() -> str:
        return "tags"
