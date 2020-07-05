from typing import List, Union
from enum import Enum

import attr

from .category import Category
from ..helpers.types import JsonData
from ..helpers.validators import validate_tag_list


def ingredient_converter(
    ingredients: Union[List["Ingredient"], List[JsonData]]
) -> List["Ingredient"]:
    final = []
    for i in ingredients:
        if isinstance(i, dict):
            final.append(Ingredient(**i))
        elif isinstance(i, Ingredient):
            final.append(i)
    return final


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
        Ingredient.verify_request_body(req)
        return Ingredient(amount=req["amount"], item=req["item"])

    @staticmethod
    def verify_request_body(body: JsonData) -> None:
        Category.verify_incoming_request(
            body=body, required_fields=["amount", "item"], optional_fields=[], category=Ingredient
        )

    @staticmethod
    def collection() -> str:
        return NotImplemented


@attr.s
class Recipe(Category):
    name: str = attr.ib()
    ingredients: List[Ingredient] = attr.ib(converter=ingredient_converter)
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
        Recipe.verify_request_body(req)
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
        Category.verify_incoming_request(
            body=body,
            required_fields=["name", "ingredients", "instructions", "recipe_type"],
            optional_fields=["cooking_style", "url", "source", "notes", "tags"],
            category=Recipe,
        )
        for ingredient in body.get("ingredients", []):
            Ingredient.verify_request_body(ingredient)

    @staticmethod
    def collection() -> str:
        return "recipes"
