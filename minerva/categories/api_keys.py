import attr

from .category import Category
from ..helpers.types import JsonData


@attr.s
class ApiKey(Category):
    key: str = attr.ib()
    user: str = attr.ib()
    id: str = attr.ib(default="")

    def __dict__(self) -> JsonData:
        return {"_id": self.id, "key": self.key, "user": self.user}

    def to_json(self) -> JsonData:
        return {"key": self.key, "user": self.user}

    @staticmethod
    def from_request(req: JsonData) -> "ApiKey":
        ApiKey.verify_request_body(req)
        return ApiKey(key=req["key"], user=req["user"])

    @staticmethod
    def verify_request_body(body: JsonData) -> None:
        Category.verify_incoming_request(
            body=body, required_fields=["key", "user"], optional_fields=[], category=ApiKey
        )

    @staticmethod
    def collection() -> str:
        return "api_keys"
