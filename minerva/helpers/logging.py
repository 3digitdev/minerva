from .types import JsonData, Maybe, LogLevel
from ..connectors.mongo import MongoConnector
from ..categories.logs import Log


def base_msg(request, message: str):
    return f"{request.method} {str(request.url_rule)} -- {message}"


def fatal(request, user: str, message: str, details: Maybe[JsonData] = None):
    with MongoConnector(Log, is_test=False) as logger:
        logger.add_log(user, LogLevel.Fatal, base_msg(request, message), details or {})


def error(request, user: str, message: str, details: Maybe[JsonData] = None):
    with MongoConnector(Log, is_test=False) as logger:
        logger.add_log(user, LogLevel.Error, base_msg(request, message), details or {})


def warn(request, user: str, message: str, details: Maybe[JsonData] = None):
    with MongoConnector(Log, is_test=False) as logger:
        logger.add_log(user, LogLevel.Warn, base_msg(request, message), details or {})


def info(request, user: str, message: str, details: Maybe[JsonData] = None):
    with MongoConnector(Log, is_test=False) as logger:
        logger.add_log(user, LogLevel.Info, base_msg(request, message), details or {})


def debug(request, user: str, message: str, details: Maybe[JsonData] = None):
    with MongoConnector(Log, is_test=False) as logger:
        logger.add_log(user, LogLevel.Debug, message, details or {})
