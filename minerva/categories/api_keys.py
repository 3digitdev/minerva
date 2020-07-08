import attr

from .category import Category
from ..helpers.types import JsonData


@attr.s
class ApiKey(Category):
    """
    These are not a standard "category" in that they do not have a set of
    CRUD endpoints, but they are still stored/retrieved from the DB.

    This is used for super-simple authentication of the user hitting the API.

    There are probably far better and more secure ways to do this, and PRs are
    welcome if you are better at this than me.  Given that this is a personal project
    in its outset, I won't be putting much effort into this...yet.
    """

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
