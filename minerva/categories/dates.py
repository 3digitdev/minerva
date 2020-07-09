from typing import List

import attr

from .category import Category
from ..helpers.custom_types import JsonData
from ..helpers.validators import validate_tag_list, day_validator, month_validator, year_validator
from ..helpers.converters import num_padding


@attr.s
class Date(Category):
    name: str = attr.ib()
    day: str = attr.ib(validator=day_validator, converter=num_padding)
    month: str = attr.ib(validator=month_validator, converter=num_padding)
    year: str = attr.ib(default="", validator=year_validator)
    subject: str = attr.ib(default="")
    notes: List[str] = attr.ib(default=[])
    # ---
    tags: List[str] = attr.ib(default=[], validator=validate_tag_list)
    id: str = attr.ib(default="")

    def __dict__(self) -> JsonData:
        return {
            "_id": self.id,
            "name": self.name,
            "day": self.day,
            "month": self.month,
            "year": self.year,
            "subject": self.subject,
            "notes": self.notes,
            "tags": self.tags,
        }

    def to_json(self) -> JsonData:
        return {
            "name": self.name,
            "day": self.day,
            "month": self.month,
            "year": self.year,
            "subject": self.subject,
            "notes": self.notes,
            "tags": self.tags,
        }

    @staticmethod
    def from_request(req: JsonData) -> "Date":
        Date.verify_request_body(req)
        return Date(
            name=req["name"],
            day=req["day"],
            month=req["month"],
            year=req.get("year", ""),
            subject=req.get("subject", ""),
            notes=req.get("notes", []),
            tags=req.get("tags", []),
        )

    @staticmethod
    def verify_request_body(body: JsonData) -> None:
        Category.verify_incoming_request(
            body=body,
            required_fields=["name", "day", "month"],
            optional_fields=["year", "subject", "notes", "tags"],
            category=Date,
        )

    @staticmethod
    def collection() -> str:
        return "dates"
