from typing import List

import attr

from .category import Category
from ..helpers.exceptions import BadRequestError
from ..helpers.types import JsonData
from ..helpers.validators import validate_tag_list


def day_validator(instance, attr, value) -> None:
    try:
        day_num = int(value)
        if not (1 <= day_num <= 31):
            raise BadRequestError(f"'day' must be a valid value between 1-31, got [{day_num}]")
        # TODO:  Validate combo of Month/Day
    except ValueError:
        raise BadRequestError(f"Could not convert 'day' value of '{value}' to an integer")


def num_padding(value: str) -> str:
    try:
        num = int(value)
        if num < 10:
            return f"0{num}"
        else:
            return str(num)
    except ValueError:
        # The validator will catch these -- this allows optional fields that are empty strings
        # to use this converter function and not bomb out.
        return value


def month_validator(instance, attr, value) -> None:
    try:
        month_num = int(value)
        if not (1 <= month_num <= 12):
            raise BadRequestError(f"'month' must be a valid value between 1-12, got [{month_num}]")
    except ValueError:
        raise BadRequestError(f"Could not convert 'month' value of '{value}' to an integer")


def year_validator(instance, attr, value) -> None:
    if value == "":
        return
    try:
        int(value)
    except ValueError:
        raise BadRequestError(f"Could not convert 'year' value of '{value}' to an integer")


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
