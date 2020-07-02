import attr

from categories.category import Category
from helpers.exceptions import BadRequestError
from helpers.helpers import JsonData


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
        return Tag(name=req["name"])

    @staticmethod
    def verify_request_body(body: JsonData) -> None:
        required = ["name"]
        for field in required:
            if field not in body:
                raise BadRequestError(f"Invalid request -- missing field '{field}' in Tag")

    @staticmethod
    def collection() -> str:
        return "tags"
