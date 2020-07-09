from typing import List

from minerva.categories.dates import Date
from minerva.categories.employments import Employment
from minerva.categories.housings import Housing
from minerva.categories.links import Link
from minerva.categories.logins import Login
from minerva.categories.notes import Note
from minerva.categories.recipes import Recipe
from minerva.categories.tags import Tag
from minerva.categories.logs import Log
from minerva.connectors.base_connector import BaseConnector
from minerva.connectors.datastore_factory import DatastoreFactory
from minerva.helpers.config_loader import load_config

collections = [Date, Employment, Housing, Link, Login, Note, Recipe, Tag]


if __name__ == "__main__":
    """
    Goes through all the unittest_<type> collections and removes all records.
    This is useful when something goes wrong and records get left over somehow.
    
    Use this from the `make clean` or `make clean_unit` Makefile targets.
    """
    print("------------------------------------")
    print("--- Cleaning Unit Test Artifacts ---")
    print("------------------------------------")
    config = load_config()
    # Not loading the Flask config, need to add this manually
    config["TESTING"] = True
    datastore = DatastoreFactory.build(config)
    print(datastore)
    for type_name in collections:
        with datastore(item_type=type_name, config=config) as db:
            deleted = db.delete_all()
            print(f"Deleted {deleted} records for {type_name.__name__}s")
    print("---------------------")
    print("--- Cleaning Logs ---")
    print("---------------------")
    with datastore(item_type=Log, config=config) as db:
        logs = db.find_all_no_limit()
        to_delete = []
        for log in logs:
            if not isinstance(log, Log):
                continue
            if log.user == "TEST_USER":
                to_delete.append(log.id)
        count = 0
        for delete_id in to_delete:
            count += 1 if db.delete_one(delete_id) else 0
        print(f"Deleted {count} records for Logs")
    print(("=" * 30))
