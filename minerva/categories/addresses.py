from typing import List

import attr

from categories.category import Category
from helpers.exceptions import BadRequestError
from helpers.types import JsonData
from helpers.validators import validate_tag_list


@attr.s
class Address(Category):
    number: str = attr.ib()
    street: str = attr.ib()
    city: str = attr.ib()
    state: str = attr.ib()
    zip_code: str = attr.ib()
    extra: str = attr.ib()  # The "second line" (apt, suite, etc.)
    # ---
    tags: List[str] = attr.ib(default=[], validator=validate_tag_list)

    def __dict__(self) -> JsonData:
        return {
            "number": self.number,
            "street": self.street,
            "extra": self.extra,
            "city": self.city,
            "state": self.state,
            "zip_code": self.zip_code,
            "tags": self.tags,
        }

    def to_json(self) -> JsonData:
        return {
            "number": self.number,
            "street": self.street,
            "extra": self.extra,
            "city": self.city,
            "state": self.state,
            "zip_code": self.zip_code,
            "tags": self.tags,
        }

    @staticmethod
    def from_request(req: JsonData) -> "Address":
        return Address(
            number=req["number"],
            street=req["street"],
            city=req["city"],
            state=req["state"],
            zip_code=req["zip_code"],
            extra=req.get("extra", ""),
            tags=req.get("tags", []),
        )

    @staticmethod
    def verify_request_body(body: JsonData) -> None:
        required = ["number", "street", "city", "state", "zip_code"]
        for field in required:
            if field not in body:
                raise BadRequestError(f"Invalid request -- missing field '{field}' in Address")

    @staticmethod
    def collection() -> str:
        # Addresses are not stored directly, but are part of other categories
        raise NotImplemented
