from typing import Dict, Any, TypeVar, Optional
from enum import Enum

JsonData = Dict[str, Any]
T = TypeVar("T")
Maybe = Optional[T]


# --- Logging --- #
class LogLevel(Enum):
    Fatal = (0,)
    Error = (1,)
    Warn = (2,)
    Info = (3,)
    Debug = 4

    def __str__(self):
        return self.name.lower()

    @staticmethod
    def from_str(level: str) -> "LogLevel":
        return {
            "fatal": LogLevel.Fatal,
            "error": LogLevel.Error,
            "warn": LogLevel.Warn,
            "info": LogLevel.Info,
            "debug": LogLevel.Debug,
        }[level.lower()]


# --------------- #
