from abc import ABCMeta, abstractmethod
from typing import List, Type

from ..helpers.exceptions import BadRequestError
from ..helpers.custom_types import JsonData


class Category(metaclass=ABCMeta):
    """
    Astract base class for all objects that are stored in the database.
    Implementing these functions allows it to be stored and retrieved easily
    """

    def __init__(self, **kwargs):
        """
        Pretty plain -- ideally new Category objects should use `attrs` to initialize
        things and reduce any boilerplate.  See existing Category objects for examples
        """
        pass

    @abstractmethod
    def __dict__(self) -> JsonData:
        """
        This is used to convert the object into a dictionary that can be
        returned as JSON in the API response body
        :return: A dictionary representation of the object, including the ID
        """
        return NotImplemented

    @abstractmethod
    def to_json(self) -> JsonData:
        """
        This is entirely used only by the Mongo connector to make a version
        of the object (without ID) that can be stored in Mongo.  Pretty much
        just a version of __dict__ but without the `_id` field.
        :return: A dictionary representation of the object **without** the ID
        """
        return NotImplemented

    @staticmethod
    @abstractmethod
    def from_request(req: JsonData) -> "Category":
        """
        Convert the Flask request body to the Category object type.
        This should always start with a call to <Type>.verify_request_body(req)
        to make sure that all required data exists.
        :param req: The Flask request body
        :return: The newly created object
        """
        return NotImplemented

    @staticmethod
    def verify_incoming_request(
        *,
        body: JsonData,
        required_fields: List[str],
        optional_fields: List[str],
        category: Type["Category"],
    ) -> None:
        """
        Helper method available to all Category objects.  Makes sure that the
        incoming request has all of the necessary fields to build the object of the
        given type, as well as not including any additional unexpected fields.
        Will raise HttpErrors when it finds something it doesn't like.
        **NOTE:  All params require qualification in the call.**
        :param body: The Flask request body to verify
        :param required_fields: A list of the required fields for the object, as strings
        :param optional_fields: A list of the optional fields for the object, as strings
        :param category:
        :return: N/A
        """
        all_fields = required_fields + optional_fields
        for field in body:
            if field not in all_fields:
                raise BadRequestError(f"Invalid request -- found unexpected field '{field}'")
        for field in required_fields:
            if field not in body:
                raise BadRequestError(
                    f"Invalid request -- missing field '{field}' in {category.__name__}"
                )
            else:
                if body[field] is None or body[field] == "":
                    raise BadRequestError(f"Invalid request -- required field '{field}' is empty")

    @staticmethod
    @abstractmethod
    def verify_request_body(body: JsonData) -> None:
        """
        A kind of "wrapper" function that allows the category to define
        its list of required and optional fields for construction.
        Some creative meta-programming could probably get around needing this,
        but there's enough of that already in this project, so let's favor readability.
        :param body: The incoming Flask request body
        :return: N/A
        """
        return NotImplemented

    @staticmethod
    @abstractmethod
    def collection() -> str:
        """
        The name of the collection that objects of this type are stored in.
        For Mongo, this is the Collection name, but it could also be used as
        a Table name for SQL-like DBs, etc.
        :return: The name of the collection
        """
        return NotImplemented

    @classmethod
    def from_mongo(cls, record: JsonData) -> "Category":
        """
        This is a mongo-specific wrapper function for handling the weird way that
        Mongo deals with unique IDs to make it work well with the base constructor
        THIS IS NOT NECESSARY FOR NON-MONGO CONSTRUCTORS.
        :param record: The Mongo record
        :return: The newly-created object from the Mongo record
        """
        record["id"] = str(record["_id"])
        del record["_id"]
        return cls(**record)
