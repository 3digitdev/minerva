from typing import List
from abc import ABCMeta, abstractmethod

from helpers.helpers import JsonData, SingleMongoRecord


class Category(metaclass=ABCMeta):
    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def __dict__(self):
        return NotImplemented

    @abstractmethod
    def to_json(self):
        return NotImplemented

    @staticmethod
    @abstractmethod
    def from_request(req: JsonData) -> "Category":
        return NotImplemented

    @staticmethod
    @abstractmethod
    def required() -> List[str]:
        return NotImplemented

    @staticmethod
    @abstractmethod
    def collection() -> str:
        return NotImplemented

    @classmethod
    def from_mongo(cls, record: SingleMongoRecord) -> "Category":
        record["id"] = str(record["_id"])
        del record["_id"]
        return cls(**record)
