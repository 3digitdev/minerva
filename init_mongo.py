from pymongo import MongoClient

collections = [
    "dates",
    "employments",
    "housings",
    "links",
    "logins",
    "access_logs",
    "notes",
    "recipes",
    "tags",
]

if __name__ == "__main__":
    client = MongoClient("mongodb://localhost:27017/")
    db = client.minerva
    for coll in collections:
        if coll not in db.list_collection_names():
            db.create_collection(coll)
    tag_coll = db["tags"]
    tag_coll.create_index("name", unique=True)
    log_coll = db["access_logs"]
    log_coll.create_index("created_at", expireAfterSeconds=604800)
