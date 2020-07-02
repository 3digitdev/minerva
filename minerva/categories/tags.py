from typing import List

import attr

from categories.category import Category
from helpers.helpers import JsonData


@attr.s
class Tag(Category):
    name: str = attr.ib()
    id: str = attr.ib(default="")

    def __dict__(self):
        return {"_id": self.id, "name": self.name}

    def to_json(self):
        return {"name": self.name}

    @staticmethod
    def from_request(req: JsonData) -> "Tag":
        return Tag(name=req["name"])

    @staticmethod
    def required() -> List[str]:
        return ["name"]

    @staticmethod
    def collection() -> str:
        return "tags"
