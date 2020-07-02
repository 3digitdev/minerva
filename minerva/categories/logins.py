from typing import List, Union

import attr

from categories.category import Category
from helpers.exceptions import BadRequestError
from helpers.helpers import JsonData


@attr.s
class SecurityQuestion(Category):
    question: str = attr.ib()
    answer: str = attr.ib()

    def __dict__(self):
        return {"question": self.question, "answer": self.answer}

    def to_json(self):
        return self.__dict__()

    @staticmethod
    def from_request(req: JsonData) -> "SecurityQuestion":
        return SecurityQuestion(
            question=req.get("question", ""), answer=req.get("answer", "")
        )

    @staticmethod
    def verify_request_body(body: JsonData) -> None:
        required = ["question", "answer"]
        for field in required:
            if field not in body:
                raise BadRequestError(
                    f"Invalid request -- missing field '{field}' in Security Question"
                )

    @staticmethod
    def collection() -> str:
        return NotImplemented


# Needed for attrs conversion
def convert_sq_list(
    inputs: List[Union[JsonData, SecurityQuestion]]
) -> List[SecurityQuestion]:
    sq_list = []
    for sq in inputs:
        if isinstance(sq, SecurityQuestion):
            sq_list.append(sq)
        elif isinstance(sq, dict):
            sq_list.append(SecurityQuestion(**sq))
        else:
            raise BadRequestError(
                f"Could not parse security questions -- was {sq.__class__}"
            )
    return sq_list


@attr.s
class Login(Category):
    application: str = attr.ib()
    password: str = attr.ib()
    url: str = attr.ib(default="")
    username: str = attr.ib(default="")
    email: str = attr.ib(default="")
    security_questions: List[SecurityQuestion] = attr.ib(
        default=[], converter=convert_sq_list
    )
    id: str = attr.ib(default="")

    def __dict__(self):
        return {
            "_id": self.id,
            "application": self.application,
            "password": self.password,
            "url": self.url,
            "username": self.username,
            "email": self.email,
            "security_questions": [sq.__dict__() for sq in self.security_questions],
        }

    def to_json(self):
        return {
            "application": self.application,
            "password": self.password,
            "url": self.url,
            "username": self.username,
            "email": self.email,
            "security_questions": [sq.to_json() for sq in self.security_questions],
        }

    @staticmethod
    def from_request(req: JsonData) -> "Login":
        login = Login(
            application=req["application"],
            password=req["password"],
            url=req.get("url", ""),
            username=req.get("username", ""),
            email=req.get("email", ""),
            security_questions=[
                SecurityQuestion.from_request(sq)
                for sq in req.get("security_questions", [])
            ],
        )
        return login

    @staticmethod
    def verify_request_body(body: JsonData) -> None:
        required = ["application", "password"]
        for field in required:
            if field not in body:
                raise BadRequestError(
                    f"Invalid request -- missing field '{field}' in Login"
                )
        for sq in body.get("security_questions", []):
            SecurityQuestion.verify_request_body(sq)

    @staticmethod
    def collection() -> str:
        return "logins"
