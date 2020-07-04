from typing import List
from enum import Enum

import attr

from .category import Category
from ..helpers.exceptions import BadRequestError
from ..helpers.types import JsonData
from ..helpers.validators import validate_tag_list


class RecipeType(str, Enum):
    Entree = "entree"
    Dessert = "dessert"
    Salad = "salad"
    Soup = "soup"
    SideDish = "side dish"
    Casserole = "casserole"
    Appetizer = "appetizer"

    def __str__(self):
        return self.value


@attr.s
class Ingredient(Category):
    amount: str = attr.ib()
    item: str = attr.ib()

    def __dict__(self) -> JsonData:
        return {"amount": self.amount, "item": self.item}

    def to_json(self) -> JsonData:
        return self.__dict__()

    @staticmethod
    def from_request(req: JsonData) -> "Ingredient":
        return Ingredient(amount=req["amount"], item=req["item"])

    @staticmethod
    def verify_request_body(body: JsonData) -> None:
        required = ["amount", "item"]
        for field in required:
            if field not in body:
                raise BadRequestError(f"Invalid request -- missing field '{field}' in Ingredient")

    @staticmethod
    def collection() -> str:
        return NotImplemented


@attr.s
class Recipe(Category):
    name: str = attr.ib()
    ingredients: List[Ingredient] = attr.ib()
    instructions: List[str] = attr.ib()
    recipe_type: RecipeType = attr.ib()
    cooking_style: str = attr.ib(default="")
    url: str = attr.ib(default="")
    source: str = attr.ib(default="")
    notes: List[str] = attr.ib(default=[])
    # ---
    tags: List[str] = attr.ib(default=[], validator=validate_tag_list)
    id: str = attr.ib(default="")

    def __dict__(self) -> JsonData:
        return {
            "_id": self.id,
            "name": self.name,
            "ingredients": [i.__dict__() for i in self.ingredients],
            "instructions": self.instructions,
            "recipe_type": str(self.recipe_type),
            "cooking_style": self.cooking_style,
            "url": self.url,
            "source": self.source,
            "notes": self.notes,
            "tags": self.tags,
        }

    def to_json(self) -> JsonData:
        return {
            "name": self.name,
            "ingredients": [i.to_json() for i in self.ingredients],
            "instructions": self.instructions,
            "recipe_type": str(self.recipe_type),
            "cooking_style": self.cooking_style,
            "url": self.url,
            "source": self.source,
            "notes": self.notes,
            "tags": self.tags,
        }

    @staticmethod
    def from_request(req: JsonData) -> "Recipe":
        return Recipe(
            name=req["name"],
            ingredients=[Ingredient.from_request(i) for i in req["ingredients"]],
            instructions=req["instructions"],
            recipe_type=req["recipe_type"],
            cooking_style=req.get("cooking_style", ""),
            url=req.get("url", ""),
            source=req.get("source", ""),
            notes=req.get("notes", []),
            tags=req.get("tags", []),
        )

    @staticmethod
    def verify_request_body(body: JsonData) -> None:
        required = ["name", "ingredients", "instructions", "recipe_type"]
        for field in required:
            if field not in body:
                raise BadRequestError(f"Invalid request -- missing field '{field}' in Recipe")

    @staticmethod
    def collection() -> str:
        return "recipes"
