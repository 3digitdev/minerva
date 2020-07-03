from typing import Type, List

from categories.category import Category
from helpers.types import JsonData, Maybe
from pymongo import MongoClient, ReturnDocument
from pymongo.database import Database
from bson.objectid import ObjectId


def by_id(obj_id: str) -> JsonData:
    return {"_id": ObjectId(obj_id)}


class MongoConnector:
    def __init__(self, item_type: Type[Category]) -> None:
        self.item_type = item_type

    def __enter__(self) -> "MongoConnector":
        self.client: MongoClient = MongoClient("mongodb://localhost:27017/")
        self.db: Database = self.client.minerva
        self.collection = self.db[self.item_type.collection()]
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

    def update_one(self, item_id: str, updated_item: Category) -> Maybe[Category]:
        result = self.collection.find_one_and_update(
            by_id(item_id), {"$set": updated_item.to_json()}, return_document=ReturnDocument.AFTER,
        )
        if result is None:
            return result
        return self.item_type.from_mongo(result)

    def tag_one(self, item_id: str, tag: str) -> Category:
        # If the tag already exists, a new one is not added
        result = self.collection.find_one_and_update(by_id(item_id), {"$addToSet": {"tags": tag}})
        return self.item_type.from_mongo(result)

    def delete_one(self, item_id: str) -> int:
        return self.collection.delete_one(by_id(item_id)).deleted_count