from typing import Type

from .custom_types import JsonData, Maybe, LogLevel
from ..connectors.base_connector import BaseConnector
from ..categories.logs import Log


def base_msg(request, message: str):
    return f"{request.method} {str(request.url_rule)} -- {message}"


class Logger:
    def __init__(self, datastore: Type[BaseConnector], config: JsonData):
        self.datastore = datastore
        self.config = config

    def fatal(self, request, user: str, message: str, details: Maybe[JsonData] = None):
        with self.datastore(Log, self.config) as logger:
            logger.add_log(user, LogLevel.Fatal, base_msg(request, message), details or {})

    def error(self, request, user: str, message: str, details: Maybe[JsonData] = None):
        with self.datastore(Log, self.config) as logger:
            logger.add_log(user, LogLevel.Error, base_msg(request, message), details or {})

    def warn(self, request, user: str, message: str, details: Maybe[JsonData] = None):
        with self.datastore(Log, self.config) as logger:
            logger.add_log(user, LogLevel.Warn, base_msg(request, message), details or {})

    def info(self, request, user: str, message: str, details: Maybe[JsonData] = None):
        with self.datastore(Log, self.config) as logger:
            logger.add_log(user, LogLevel.Info, base_msg(request, message), details or {})

    def debug(self, request, user: str, message: str, details: Maybe[JsonData] = None):
        with self.datastore(Log, self.config) as logger:
            logger.add_log(user, LogLevel.Debug, base_msg(request, message), details or {})
