import attr


@attr.s
class Note:
    id: int = attr.ib()
    content: str = attr.ib()
    url: str = attr.ib(default="")

    def __dict__(self):
        return {"id": self.id, "content": self.content, "url": self.url}
