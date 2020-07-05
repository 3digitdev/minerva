from typing import List, Union

import attr

from .category import Category
from ..helpers.exceptions import BadRequestError
from ..helpers.types import JsonData
from ..helpers.validators import validate_tag_list


@attr.s
class SecurityQuestion(Category):
    question: str = attr.ib()
    answer: str = attr.ib()

    def __dict__(self) -> JsonData:
        return {"question": self.question, "answer": self.answer}

    def to_json(self) -> JsonData:
        return self.__dict__()

    @staticmethod
    def from_request(req: JsonData) -> "SecurityQuestion":
        SecurityQuestion.verify_request_body(req)
        return SecurityQuestion(question=req.get("question", ""), answer=req.get("answer", ""))

    @staticmethod
    def verify_request_body(body: JsonData) -> None:
        Category.verify_incoming_request(
            body=body,
            required_fields=["question", "answer"],
            optional_fields=[],
            category=SecurityQuestion,
        )

    @staticmethod
    def collection() -> str:
        return NotImplemented


# Needed for attrs conversion
def convert_sq_list(inputs: List[Union[JsonData, SecurityQuestion]]) -> List[SecurityQuestion]:
    sq_list = []
    for sq in inputs:
        if isinstance(sq, SecurityQuestion):
            sq_list.append(sq)
        elif isinstance(sq, dict):
            sq_list.append(SecurityQuestion(**sq))
        else:
            raise BadRequestError(
                f"Could not parse security questions -- was [{sq.__class__.__name__}]"
            )
    return sq_list


@attr.s
class Login(Category):
    application: str = attr.ib()
    password: str = attr.ib()
    url: str = attr.ib(default="")
    username: str = attr.ib(default="")
    email: str = attr.ib(default="")
    security_questions: List[SecurityQuestion] = attr.ib(default=[], converter=convert_sq_list)
    # ---
    tags: List[str] = attr.ib(default=[], validator=validate_tag_list)
    id: str = attr.ib(default="")

    def __dict__(self) -> JsonData:
        return {
            "_id": self.id,
            "application": self.application,
            "password": self.password,
            "url": self.url,
            "username": self.username,
            "email": self.email,
            "security_questions": [sq.__dict__() for sq in self.security_questions],
            "tags": self.tags,
        }

    def to_json(self) -> JsonData:
        return {
            "application": self.application,
            "password": self.password,
            "url": self.url,
            "username": self.username,
            "email": self.email,
            "security_questions": [sq.to_json() for sq in self.security_questions],
            "tags": self.tags,
        }

    @staticmethod
    def from_request(req: JsonData) -> "Login":
        Login.verify_request_body(req)
        return Login(
            application=req["application"],
            password=req["password"],
            url=req.get("url", ""),
            username=req.get("username", ""),
            email=req.get("email", ""),
            security_questions=[
                SecurityQuestion.from_request(sq) for sq in req.get("security_questions", [])
            ],
            tags=req.get("tags", []),
        )

    @staticmethod
    def verify_request_body(body: JsonData) -> None:
        Category.verify_incoming_request(
            body=body,
            required_fields=["application", "password"],
            optional_fields=["url", "username", "email", "security_questions", "tags"],
            category=Login,
        )
        for sq in body.get("security_questions", []):
            SecurityQuestion.verify_request_body(sq)

    @staticmethod
    def collection() -> str:
        return "logins"
