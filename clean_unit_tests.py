from minerva.categories.dates import Date
from minerva.categories.employments import Employment
from minerva.categories.housings import Housing
from minerva.categories.links import Link
from minerva.categories.logins import Login
from minerva.categories.notes import Note
from minerva.categories.recipes import Recipe
from minerva.categories.tags import Tag
from minerva.connectors.mongo import MongoConnector

collections = [Date, Employment, Housing, Link, Login, Note, Recipe, Tag]


if __name__ == "__main__":
    """
    Goes through all the unittest_<type> collections and removes all records.
    This is useful when something goes wrong and records get left over somehow.
    
    Use this from the `make clean` or `make clean_unit` Makefile targets.
    """
    for type_name in collections:
        with MongoConnector(item_type=type_name, is_test=True) as db:
            deleted = db.delete_all()
            print(f"deleted {deleted} records for {type_name.__name__}s")
