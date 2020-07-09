from ..connectors.mongo import MongoConnector
from ..categories.api_keys import ApiKey
from .custom_types import Maybe
from .exceptions import UnauthorizedError


def validate_key(key: Maybe[str]) -> Maybe[ApiKey]:
    """
    Validates the API key provided to make sure it exists in the DB
    TODO:  This needs to stop using the MongoConnector explicitly
    :param key: The API key value passed by the API user as an x-api-key header
    :return: The created ApiKey object if it matches the datastore, otherwise None
    """
    if not key:
        raise UnauthorizedError()
    with MongoConnector(ApiKey, is_test=False) as db:
        api_key = db.find_api_key(key)
        if not api_key:
            raise UnauthorizedError()
    return api_key
