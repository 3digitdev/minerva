from typing import List

import attr

from .addresses import Address, address_converter
from .category import Category
from ..helpers.custom_types import JsonData
from ..helpers.validators import validate_tag_list, month_validator, year_validator


@attr.s
class Housing(Category):
    address: Address = attr.ib(converter=address_converter)
    start_month: str = attr.ib(validator=month_validator)
    start_year: str = attr.ib(validator=year_validator)
    end_month: str = attr.ib(default="")
    end_year: str = attr.ib(default="")
    monthly_payment: int = attr.ib(default=0)  # mortgage, rent, etc.
    # ---
    tags: List[str] = attr.ib(default=[], validator=validate_tag_list)
    id: str = attr.ib(default="")

    def __dict__(self) -> JsonData:
        return {
            "_id": self.id,
            "address": self.address.__dict__(),
            "start_month": self.start_month,
            "start_year": self.start_year,
            "end_month": self.end_month,
            "end_year": self.end_year,
            "monthly_payment": self.monthly_payment,
            "tags": self.tags,
        }

    def to_json(self) -> JsonData:
        return {
            "address": self.address.to_json(),
            "start_month": self.start_month,
            "start_year": self.start_year,
            "end_month": self.end_month,
            "end_year": self.end_year,
            "monthly_payment": self.monthly_payment,
            "tags": self.tags,
        }

    @staticmethod
    def from_request(req: JsonData) -> "Housing":
        Housing.verify_request_body(req)
        return Housing(
            address=Address.from_request(req["address"]),
            start_month=req["start_month"],
            start_year=req["start_year"],
            end_month=req.get("end_month", ""),
            end_year=req.get("end_year", ""),
            monthly_payment=req.get("monthly_payment", 0),
            tags=req.get("tags", []),
        )

    @staticmethod
    def verify_request_body(body: JsonData) -> None:
        Category.verify_incoming_request(
            body=body,
            required_fields=["address", "start_month", "start_year"],
            optional_fields=["end_month", "end_year", "monthly_payment", "tags"],
            category=Housing,
        )
        Address.verify_request_body(body["address"])

    @staticmethod
    def collection() -> str:
        return "housings"
