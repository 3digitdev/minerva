from typing import Type

from categories.category import Category
from helpers.helpers import *
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

    def find_all(self, page: int = 1, count: int = 10) -> MultiMongoRecord:
        results = self.collection.find().skip((page - 1) * count).limit(count)
        found = []
        for item in results:
            parsed_item = self.item_type.from_mongo(item)
            found.append(parsed_item.__dict__())
        return found

    def find_one(self, item_id: str) -> Maybe[SingleMongoRecord]:
        return self.collection.find_one(by_id(item_id))

    def update_one(self, item_id: str, updated_item: Category) -> Maybe[SingleMongoRecord]:
        result = self.collection.find_one_and_update(
            by_id(item_id), {"$set": updated_item.to_json()}, return_document=ReturnDocument.AFTER,
        )
        if result is None:
            return result
        return self.item_type.from_mongo(result).__dict__()

    def tag_one(self, item_id: str, tag: str) -> SingleMongoRecord:
        # If the tag already exists, a new one is not added
        return self.collection.find_one_and_update(by_id(item_id), {"$addToSet": {"tags": tag}})

    def delete_one(self, item_id: str) -> int:
        return self.collection.delete_one(by_id(item_id)).deleted_count
