from typing import Union

import attr

from .category import Category
from ..helpers.types import JsonData


def address_converter(address: Union["Address", JsonData]) -> "Address":
    if isinstance(address, Address):
        return address
    return Address(**address)


@attr.s
class Address(Category):
    number: str = attr.ib()
    street: str = attr.ib()
    city: str = attr.ib()
    state: str = attr.ib()
    zip_code: str = attr.ib()
    extra: str = attr.ib()  # The "second line" (apt, suite, etc.)

    def __dict__(self) -> JsonData:
        return {
            "number": self.number,
            "street": self.street,
            "extra": self.extra,
            "city": self.city,
            "state": self.state,
            "zip_code": self.zip_code,
        }

    def to_json(self) -> JsonData:
        return {
            "number": self.number,
            "street": self.street,
            "extra": self.extra,
            "city": self.city,
            "state": self.state,
            "zip_code": self.zip_code,
        }

    @staticmethod
    def from_request(req: JsonData) -> "Address":
        Address.verify_request_body(req)
        return Address(
            number=req["number"],
            street=req["street"],
            city=req["city"],
            state=req["state"],
            zip_code=req["zip_code"],
            extra=req.get("extra", ""),
        )

    @staticmethod
    def verify_request_body(body: JsonData) -> None:
        Category.verify_incoming_request(
            body=body,
            required_fields=["number", "street", "city", "state", "zip_code"],
            optional_fields=["extra"],
            category=Address,
        )

    @staticmethod
    def collection() -> str:
        # Addresses are not stored directly, but are part of other categories
        raise NotImplemented
