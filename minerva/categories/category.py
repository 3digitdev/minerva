from abc import ABCMeta, abstractmethod
from typing import List, Type

from ..helpers.exceptions import BadRequestError
from ..helpers.types import JsonData


class Category(metaclass=ABCMeta):
    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def __dict__(self) -> JsonData:
        return NotImplemented

    @abstractmethod
    def to_json(self) -> JsonData:
        return NotImplemented

    @staticmethod
    @abstractmethod
    def from_request(req: JsonData) -> "Category":
        return NotImplemented

    @staticmethod
    def verify_incoming_request(
        *,
        body: JsonData,
        required_fields: List[str],
        optional_fields: List[str],
        category: Type["Category"],
    ) -> None:
        all_fields = required_fields + optional_fields
        for field in body:
            if field not in all_fields:
                raise BadRequestError(f"Invalid request -- found unexpected field '{field}'")
        for field in required_fields:
            if field not in body:
                raise BadRequestError(
                    f"Invalid request -- missing field '{field}' in {category.__name__}"
                )

    @staticmethod
    @abstractmethod
    def verify_request_body(body: JsonData) -> None:
        return NotImplemented

    @staticmethod
    @abstractmethod
    def collection() -> str:
        return NotImplemented

    @classmethod
    def from_mongo(cls, record: JsonData) -> "Category":
        record["id"] = str(record["_id"])
        del record["_id"]
        return cls(**record)
