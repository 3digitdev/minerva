from typing import Type

from ..connectors.base_connector import BaseConnector
from ..categories.api_keys import ApiKey
from .custom_types import Maybe, JsonData
from .exceptions import UnauthorizedError


def validate_key(
    key: Maybe[str], datastore: Type[BaseConnector], config: JsonData
) -> Maybe[ApiKey]:
    """
    Validates the API key provided to make sure it exists in the DB
    :param key: The API key value passed by the API user as an x-api-key header
    :param datastore: The datastore type to use for finding the API key
    :param config: The application config from 'minerva_config.json'
    :return: The created ApiKey object if it matches the datastore, otherwise None
    """
    if not key:
        raise UnauthorizedError()
    with datastore(ApiKey, config=config) as db:
        api_key = db.find_api_key(key)
        if not api_key:
            raise UnauthorizedError()
    return api_key
