from typing import List, Union

import attr

from .addresses import Address, address_converter
from .dates import month_validator, year_validator, num_padding
from .category import Category
from ..helpers.custom_types import JsonData
from ..helpers.validators import validate_tag_list


def employer_converter(employer: Union["Employer", JsonData]) -> "Employer":
    if isinstance(employer, Employer):
        return employer
    return Employer(**employer)


@attr.s
class Employer(Category):
    address: Address = attr.ib(converter=address_converter)
    phone: str = attr.ib()
    supervisor: str = attr.ib(default="")

    def __dict__(self) -> JsonData:
        return {
            "address": self.address.__dict__(),
            "phone": self.phone,
            "supervisor": self.supervisor,
        }

    def to_json(self) -> JsonData:
        return {
            "address": self.address.to_json(),
            "phone": self.phone,
            "supervisor": self.supervisor,
        }

    @staticmethod
    def from_request(req: JsonData) -> "Employer":
        Employer.verify_request_body(req)
        return Employer(
            address=Address.from_request(req["address"]),
            phone=req["phone"],
            supervisor=req.get("supervisor", ""),
        )

    @staticmethod
    def verify_request_body(body: JsonData) -> None:
        Category.verify_incoming_request(
            body=body,
            required_fields=["address", "phone"],
            optional_fields=["supervisor"],
            category=Employer,
        )
        Address.verify_request_body(body["address"])

    @staticmethod
    def collection() -> str:
        return NotImplemented


@attr.s
class Employment(Category):
    title: str = attr.ib()
    salary: int = attr.ib()
    employer: Employer = attr.ib(converter=employer_converter)
    start_month: str = attr.ib(validator=month_validator, converter=num_padding)
    start_year: str = attr.ib(validator=year_validator, converter=num_padding)
    end_month: str = attr.ib(default="", converter=num_padding)
    end_year: str = attr.ib(default="", converter=num_padding)
    # ---
    tags: List[str] = attr.ib(default=[], validator=validate_tag_list)
    id: str = attr.ib(default="")

    def __dict__(self) -> JsonData:
        return {
            "_id": self.id,
            "title": self.title,
            "salary": self.salary,
            "employer": self.employer.__dict__(),
            "start_month": self.start_month,
            "start_year": self.start_year,
            "end_month": self.end_month,
            "end_year": self.end_year,
            "tags": self.tags,
        }

    def to_json(self) -> JsonData:
        return {
            "title": self.title,
            "salary": self.salary,
            "employer": self.employer.to_json(),
            "start_month": self.start_month,
            "start_year": self.start_year,
            "end_month": self.end_month,
            "end_year": self.end_year,
            "tags": self.tags,
        }

    @staticmethod
    def from_request(req: JsonData) -> "Employment":
        Employment.verify_request_body(req)
        return Employment(
            title=req["title"],
            salary=req["salary"],
            employer=Employer.from_request(req["employer"]),
            start_month=req["start_month"],
            start_year=req["start_year"],
            end_month=req.get("end_month", ""),
            end_year=req.get("end_year", ""),
            tags=req.get("tags", []),
        )

    @staticmethod
    def verify_request_body(body: JsonData) -> None:
        Category.verify_incoming_request(
            body=body,
            required_fields=["title", "salary", "employer", "start_month", "start_year"],
            optional_fields=["tags", "end_month", "end_year"],
            category=Employment,
        )

    @staticmethod
    def collection() -> str:
        return "employments"
