import sys
from typing import Type

from ..helpers.custom_types import JsonData
from .base_connector import BaseConnector
from .mongo import MongoConnector

DB_TYPE_MAP = {
    "mongo": MongoConnector,
}


class DatastoreFactory:
    @staticmethod
    def build(config: JsonData) -> Type[BaseConnector]:
        db_type_val = config.get("database", None)
        if not db_type_val:
            print("[Setup Error]  Missing 'database' key from minerva_config.json")
            sys.exit(1)
        db_type = DB_TYPE_MAP.get(db_type_val.lower(), None)
        if not db_type:
            print(f"[Setup Error]  '{db_type_val}' is not a valid database type")
            print(f"Valid options:  {', '.join(list(DB_TYPE_MAP.keys()))}")
            sys.exit(1)
        return db_type
