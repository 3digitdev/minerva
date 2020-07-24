import os

from typing import Type, List
from bson import ObjectId
from pymongo import MongoClient, ReturnDocument
from pymongo.collection import Collection
from pymongo.database import Database
from datetime import date, datetime

from .base_connector import BaseConnector
from ..categories.api_keys import ApiKey
from ..categories.category import Category
from ..categories.logs import Log
from ..helpers.exceptions import InternalServerError
from ..helpers.custom_types import JsonData, Maybe, LogLevel


def by_id(obj_id: str) -> JsonData:
    """Helper function for building Mongo queries"""
    return {"_id": ObjectId(obj_id)}


class MongoConnector(BaseConnector):
    def __init__(self, item_type: Type[Category], is_test=False) -> None:
        super().__init__(item_type, is_test)
        self.coll_name = item_type.collection()
        if is_test:
            self.coll_name = f"unittest_{self.coll_name}"

    def __enter__(self) -> "MongoConnector":
        mongo_url = os.getenv("MONGO_URL")
        if mongo_url == "":
            raise InternalServerError("MONGO_URL not set correctly")
        self.client: MongoClient = MongoClient(mongo_url)
        self.db: Database = self.client.minerva
        self.collection: Collection = self.db[self.coll_name]
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.client.close()

    def create(self, item: Category) -> str:
        return str(self.collection.insert_one(item.to_json()).inserted_id)

    def find_all(self, page: int = 1, count: int = 10) -> List[Category]:
        results = self.collection.find().skip((page - 1) * count).limit(count)
        return [self.item_type.from_mongo(item) for item in results]

    def find_all_no_limit(self) -> List[Category]:
        results = self.collection.find()
        return [self.item_type.from_mongo(item) for item in results]

    def find_one(self, item_id: str) -> Maybe[Category]:
        result = self.collection.find_one(by_id(item_id))
        if not result:
            return None
        return self.item_type.from_mongo(result)

    def find_api_key(self, key: str) -> Maybe[ApiKey]:
        result = self.collection.find_one({"key": key})
        if not result:
            return None
        return ApiKey.from_mongo(result)

    def update_one(self, item_id: str, updated_item: Category) -> Maybe[Category]:
        result = self.collection.find_one_and_update(
            by_id(item_id), {"$set": updated_item.to_json()}, return_document=ReturnDocument.AFTER,
        )
        if result is None:
            return result
        return self.item_type.from_mongo(result)

    def tag_one(self, item_id: str, tag: str) -> Maybe[Category]:
        # If the tag already exists, a new one is not added
        result = self.collection.find_one_and_update(by_id(item_id), {"$addToSet": {"tags": tag}})
        if result is None:
            return result
        return self.item_type.from_mongo(result)

    def delete_one(self, item_id: str) -> bool:
        return self.collection.delete_one(by_id(item_id)).deleted_count > 0

    def delete_all(self) -> int:
        return self.collection.delete_many({}).deleted_count

    def get_today_events(self) -> List[Category]:
        today = date.today()
        result = self.collection.find({"month": today.strftime("%m"), "day": today.strftime("%d")})
        if result is None:
            return []
        return [self.item_type.from_mongo(event) for event in result]

    def cascade_tag_delete(self, tag_name: str) -> None:
        self.collection.update_many(
            filter={"tags": {"$in": [tag_name]}}, update={"$pullAll": {"tags": [tag_name]}}
        )

    def cascade_tag_update(self, old_tag_name: str, new_tag_name: str) -> None:
        self.collection.update_many(
            filter={"tags": {"$in": [old_tag_name]}},
            update={"$set": {"tags.$[elem]": new_tag_name}},
            array_filters=[{"elem": {"$eq": old_tag_name}}],
        )

    def add_log(self, user: str, level: LogLevel, message: str, details: JsonData = {}) -> None:
        self.collection.insert_one(
            {
                "created_at": datetime.now(),
                "user": user,
                "level": str(level),
                "message": message,
                "details": details,
            }
        )

    def get_logs(self, users: List[str] = [], levels: List[str] = []) -> List[Log]:
        search_filter = {}
        if users:
            search_filter["user"] = {"$in": users}
        if levels:
            search_filter["level"] = {"$in": levels}
        results = self.collection.find(search_filter)
        return [Log.from_mongo(log) for log in results]
