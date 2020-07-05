from abc import ABCMeta, abstractmethod
from typing import List
from bson.objectid import ObjectId

from ..categories.logs import Log
from ..categories.category import Category
from ..helpers.types import JsonData, Maybe, LogLevel


def by_id(obj_id: str) -> JsonData:
    return {"_id": ObjectId(obj_id)}


class BaseConnector(metaclass=ABCMeta):
    @abstractmethod
    def __enter__(self) -> "BaseConnector":
        return NotImplemented

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        return NotImplemented

    def create(self, item: Category) -> str:
        return NotImplemented

    def find_all(self, page: int = 1, count: int = 10) -> List[Category]:
        return NotImplemented

    def find_all_no_limit(self) -> List[Category]:
        return NotImplemented

    def find_one(self, item_id: str) -> Maybe[Category]:
        return NotImplemented

    def find_custom_filter(self, custom_filter: JsonData) -> Maybe[Category]:
        return NotImplemented

    def update_one(self, item_id: str, updated_item: Category) -> Maybe[Category]:
        return NotImplemented

    def tag_one(self, item_id: str, tag: str) -> Category:
        return NotImplemented

    def delete_one(self, item_id: str) -> int:
        return NotImplemented

    def delete_all(self) -> int:
        return NotImplemented

    def get_today_events(self) -> Maybe[List[Category]]:
        return NotImplemented

    def cascade_tag_delete(self, tag_name: str) -> None:
        return NotImplemented

    def cascade_tag_update(self, old_tag_name: str, new_tag_name: str) -> None:
        return NotImplemented

    def add_log(self, user: str, level: LogLevel, message: str, details: JsonData = {}) -> None:
        return NotImplemented

    def get_logs(self, users: List[str] = [], levels: List[str] = []) -> List[Log]:
        return NotImplemented
