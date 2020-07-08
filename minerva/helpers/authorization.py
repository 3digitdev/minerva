from ..connectors.mongo import MongoConnector
from ..categories.api_keys import ApiKey
from .types import Maybe
from .exceptions import UnauthorizedError


def validate_key(key: Maybe[str]) -> Maybe[ApiKey]:
    if not key:
        raise UnauthorizedError()
    with MongoConnector(ApiKey, is_test=False) as db:
        api_key = db.find_api_key(key)
        if not api_key:
            raise UnauthorizedError()
    return api_key
