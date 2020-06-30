from categories.notes import Note
from helpers.helpers import *
from pymongo import MongoClient, ReturnDocument
from pymongo.database import Database, Collection
from bson.objectid import ObjectId


class MongoConnector:
    def __enter__(self):
        self.client: MongoClient = MongoClient("mongodb://localhost:27017/")
        self.db: Database = self.client.minerva
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

    def _by_id(self, id: str):
        return {"_id": ObjectId(id)}

    # --- Notes --- #
    def create_note(self, note: Note) -> str:
        notes: Collection = self.db.notes
        return str(notes.insert_one(note.to_json()).inserted_id)

    def find_all_notes(self, page: int = 1, count: int = 10) -> MultiMongoRecord:
        notes: Collection = self.db.notes
        results = notes.find().skip((page - 1) * count).limit(count)
        found_notes = []
        for note in results:
            parsed_note = Note(
                id=str(note["_id"]), contents=note["contents"], url=note["url"]
            )
            found_notes.append(parsed_note.__dict__())
        return found_notes

    def find_single_note(self, note_id: str) -> Maybe[SingleMongoRecord]:
        notes: Collection = self.db.notes
        return notes.find_one(self._by_id(note_id))

    def update_note(self, note_id: str, updated_note: Note) -> Maybe[SingleMongoRecord]:
        # If "url" is None and the document updated has a URL,
        # it will be updated with an empty string
        notes: Collection = self.db.notes
        result = notes.find_one_and_update(
            self._by_id(note_id),
            {"$set": updated_note.to_json()},
            return_document=ReturnDocument.AFTER,
        )
        if result is None:
            return result
        return Note(
            id=str(result["_id"]), contents=result["contents"], url=result["url"]
        ).__dict__()

    def tag_note(self, note_id: str, tag: str) -> SingleMongoRecord:
        # If the tag already exists, a new one is not added
        notes: Collection = self.db.notes
        return notes.find_one_and_update(
            self._by_id(note_id), {"$addToSet": {"tags": tag}}
        )

    def delete_note(self, note_id: str) -> int:
        notes: Collection = self.db.notes
        return notes.delete_one(self._by_id(note_id)).deleted_count
