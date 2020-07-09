from abc import ABCMeta, abstractmethod
from typing import List, Type

from ..categories.api_keys import ApiKey
from ..categories.logs import Log
from ..categories.category import Category
from ..helpers.custom_types import JsonData, Maybe, LogLevel


class BaseConnector(metaclass=ABCMeta):
    """
    Abstract base class for any data-storage mechanism.  Every connector that implements these
    functions in a way that makes sense best for that storage mechanism should do just fine.
    """

    def __init__(self, item_type: Type[Category], config: JsonData) -> None:
        """
        Constructor for the connector.  Do any additional setup needed for config etc. here
        :param item_type: The type of "Category" object
        :param config: Data loaded from 'minerva_config.json'
        """
        self.item_type = item_type
        self.is_test = config.get("TESTING", False)
        self.host = config.get("host")
        self.port = config.get("port")

    @abstractmethod
    def __enter__(self) -> "BaseConnector":
        return NotImplemented

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        CLEAN UP AFTER YOURSELF!
        """
        return NotImplemented

    @abstractmethod
    def create(self, item: Category) -> str:
        """
        Insert a single new "Category" object into the store
        :param item: The object to be created
        :return: The unique ID of the object that was created
        """
        return NotImplemented

    @abstractmethod
    def find_all(self, page: int = 1, count: int = 10) -> List[Category]:
        """
        Retrieve a paginated list of all of a single type of "Category" object
        :param page: The **1-indexed** page number to be retrieving
        :param count: The number of items to retrieve in a single page
        :return: A list of "Category" objects retrieved with the query
        """
        return NotImplemented

    @abstractmethod
    def find_all_no_limit(self) -> List[Category]:
        """
        Like find_all(), but with no pagination.  This would only be used sparingly!
        :return: A list of every single object of a specific "Category" type in the store
        """
        return NotImplemented

    @abstractmethod
    def find_one(self, item_id: str) -> Maybe[Category]:
        """
        Find a single "Category" object by its unique ID
        :param item_id: The unique ID of the object in the store
        :return: The object found with the ID, or None if the ID didn't match an entry
        """
        return NotImplemented

    @abstractmethod
    def find_api_key(self, key: str) -> Maybe[ApiKey]:
        """
        Find an API key in the store by the key text
        :param key: The key text for the API key passed from the API consumer
        :return: The ApiKey object if found, otherwise None
        """
        return NotImplemented

    @abstractmethod
    def update_one(self, item_id: str, updated_item: Category) -> Maybe[Category]:
        """
        Update a single "Category" object in the store.  This is intended as a _full_
        update, not a patch update.  The entire provided updated_item should replace
        the object in the store.
        :param item_id: The unique ID of the object to update
        :param updated_item: The new values to update the object with.
        :return: The updated object if found, otherwise None
        """
        return NotImplemented

    @abstractmethod
    def tag_one(self, item_id: str, tag: str) -> Maybe[Category]:
        """
        Add an existing Tag name to a "Category" object in the store.  This
        operation is "idempotent"; that is, if the object already has this tag,
        then nothing should change but the operation should still succeed.
        :param item_id: The unique ID of the object to tag
        :param tag: The name of the tag to apply to the object
        :return: The updated object with the new tag if found, otherwise None
        """
        return NotImplemented

    @abstractmethod
    def delete_one(self, item_id: str) -> bool:
        """
        Delete a single "Category" object from the store by ID
        :param item_id: The unique ID of the object to delete
        :return: Whether the result deleted an object or not.  For a datastore that
                 cannot determine this without another query, it's best to just return True.
        """
        return NotImplemented

    @abstractmethod
    def delete_all(self) -> int:
        """
        Delete all records of a single "Category" object type from the store
        :return: The number of records deleted from the store
        """
        return NotImplemented

    @abstractmethod
    def get_today_events(self) -> List[Category]:
        """
        A special function to get a list of all "Date" Category objects from the
        store that match to the date when the function was called.
        :return: A list of the "Date" Category objects that match today's date; can be empty.
        """
        return NotImplemented

    @abstractmethod
    def cascade_tag_delete(self, tag_name: str) -> None:
        """
        A special function used when a "Tag" object is deleted from the store.
        This should search through all existing "Category" objects and delete the name
        of the tag that was passed to the function from the list of tags for each object.
        :param tag_name: The name of the Tag to delete from records
        :return: N/A
        """
        return NotImplemented

    @abstractmethod
    def cascade_tag_update(self, old_tag_name: str, new_tag_name: str) -> None:
        """
        A special function used when a "Tag" object's name is update in the store.
        This should search through all existing "Category" objects and update the name
        of the tag that was passed to the function in the list of tags for each object.
        :param old_tag_name: The previous name of the Tag
        :param new_tag_name: The updated name of the Tag
        :return: N/A
        """
        return NotImplemented

    @abstractmethod
    def add_log(self, user: str, level: LogLevel, message: str, details: JsonData = {}) -> None:
        """
        Create a new Log entry in the database.  Ideally, the database should be auto-deleting
        Log objects after a set period (recommend 7 days)
        :param user: The user that triggered the action
        :param level: The level of the log (Fatal|Error|Warn|Info|Debug)
        :param message: The message to put in the logs.  **No extra formatting on this should be needed.**
        :param details: Extra details about the message.  This is implemented as a key-value dict.
                        For datastores that don't handle that well, it's recommended to
                        `json.dumps()` this param to be stored as a simple string
        :return: N/A
        """
        return NotImplemented

    @abstractmethod
    def get_logs(self, users: List[str] = [], levels: List[str] = []) -> List[Log]:
        """
        Retrieve a list of all Log entries in the store, possibly with filters applied
        :param users: A list of usernames to filter logs by
        :param levels: A list of log levels to filter logs by (standard log levels)
        :return: A list of the Log entries found, filtered as needed; can be empty
        """
        return NotImplemented
