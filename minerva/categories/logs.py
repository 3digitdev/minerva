import attr

from datetime import datetime

from .category import Category
from ..helpers.custom_types import JsonData, LogLevel


@attr.s
class Log(Category):
    created_at: datetime = attr.ib()
    user: str = attr.ib()
    level: LogLevel = attr.ib(converter=LogLevel.from_str)
    message: str = attr.ib()
    details: JsonData = attr.ib(default={})
    # ---
    id: str = attr.ib(default="")

    def __dict__(self) -> JsonData:
        return {
            "_id": self.id,
            "created_at": self.created_at.isoformat(),
            "user": self.user,
            "level": str(self.level),
            "message": self.message,
            "details": self.details,
        }

    def to_json(self) -> JsonData:
        return {
            "created_at": self.created_at,
            "user": self.user,
            "level": str(self.level),
            "message": self.message,
            "details": self.details,
        }

    @staticmethod
    def from_request(req: JsonData) -> "Category":
        # Not needed for logs
        return NotImplemented

    @staticmethod
    def verify_request_body(body: JsonData) -> None:
        # Not needed for logs
        return NotImplemented

    @staticmethod
    def collection() -> str:
        return "access_logs"
