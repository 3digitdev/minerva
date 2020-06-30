from typing import List

import attr

from helpers.helpers import JsonData


@attr.s
class Note:
    contents: str = attr.ib()
    url: str = attr.ib(default="")
    id: str = attr.ib(default="")

    def __dict__(self):
        return {"_id": self.id, "contents": self.contents, "url": self.url}

    def to_json(self):
        return {"contents": self.contents, "url": self.url}

    @staticmethod
    def from_request(req: JsonData) -> "Note":
        note = Note(contents=req["contents"])
        if "url" in req:
            note.url = req["url"]
        return note

    @staticmethod
    def required() -> List[str]:
        return ["contents"]
