from typing import List

import attr

from .addresses import Address
from .category import Category
from ..helpers.exceptions import BadRequestError
from ..helpers.types import JsonData
from ..helpers.validators import validate_tag_list


@attr.s
class Employer(Category):
    address: Address = attr.ib()
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
        required = ["address", "phone"]
        for field in required:
            if field not in body:
                raise BadRequestError(f"Invalid request -- missing field '{field}' in Employer")

    @staticmethod
    def collection() -> str:
        return NotImplemented


@attr.s
class Employment(Category):
    title: str = attr.ib()
    salary: int = attr.ib()
    employer: Employer = attr.ib()
    # ---
    tags: List[str] = attr.ib(default=[], validator=validate_tag_list)
    id: str = attr.ib(default="")

    def __dict__(self) -> JsonData:
        return {
            "_id": self.id,
            "title": self.title,
            "salary": self.salary,
            "employer": self.employer.__dict__(),
            "tags": self.tags,
        }

    def to_json(self) -> JsonData:
        return {
            "_id": self.id,
            "title": self.title,
            "salary": self.salary,
            "employer": self.employer.to_json(),
            "tags": self.tags,
        }

    @staticmethod
    def from_request(req: JsonData) -> "Employment":
        Employment.verify_request_body(req)
        return Employment(
            title=req["title"],
            salary=req["salary"],
            employer=Employer.from_request(req["employer"]),
            tags=req.get("tags", []),
        )

    @staticmethod
    def verify_request_body(body: JsonData) -> None:
        required = ["title", "salary", "employer"]
        for field in required:
            if field not in body:
                raise BadRequestError(f"Invalid request -- missing field '{field}' in Employment")

    @staticmethod
    def collection() -> str:
        return "employments"
