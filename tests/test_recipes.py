from minerva import MongoConnector
from minerva.categories.recipes import Recipe, RecipeType
from .test_categories_base import CategoriesTestsBase


class RecipesTests(CategoriesTestsBase):
    def setUp(self) -> None:
        self.item_type = Recipe
        super().setUp()
        self.test_recipes = [
            {
                "name": "Creme Fraiche",
                "ingredients": [
                    {"amount": "1/2", "item": "creme"},
                    {"amount": "1/2", "item": "fraiche"},
                ],
                "instructions": ["combine", "serve"],
                "recipe_type": RecipeType.Dessert,
                "cooking_style": "Frozen",
                "url": "google.com",
                "source": "South Park",
                "notes": ["CREME", "FRAICHE"],
                "tags": [],
            },
            {
                "name": "Scalloped Potatoes",
                "ingredients": [{"amount": "", "item": "potatoes"}],
                "instructions": ["scallop", "eat"],
                "recipe_type": RecipeType.SideDish,
                "cooking_style": "Baked",
                "url": "google.com",
                "source": "The Almighty",
                "notes": [],
                "tags": [],
            },
        ]
        with MongoConnector(Recipe, is_test=True) as db:
            for recipe in self.test_recipes:
                self.ids_to_cleanup.append(db.create(Recipe.from_request(recipe)))

    def tearDown(self) -> None:
        super().tearDown()

    # region Create
    def test_create_recipe(self):
        response = self.verify_response_code(
            self.app.post(
                "/api/v1/recipes",
                json={
                    "name": "Marshmallows",
                    "ingredients": [{"amount": "all", "item": "marshmallow"},],
                    "instructions": ["mix"],
                    "recipe_type": RecipeType.Dessert,
                    "cooking_style": "",
                    "url": "",
                    "source": "",
                    "notes": [],
                    "tags": [],
                },
            ),
            201,
        )
        new_id = self.assertFieldIn(response, field="id")
        self.ids_to_cleanup.append(new_id)

    def test_create_recipe_missing_required_field(self):
        self.verify_response_code(
            self.app.post(
                "/api/v1/recipes",
                json={
                    "ingredients": [{"amount": "all", "item": "marshmallow"},],
                    "instructions": ["mix"],
                    "recipe_type": RecipeType.Dessert,
                    "cooking_style": "",
                    "url": "",
                    "source": "",
                    "notes": [],
                    "tags": [],
                },
            ),
            400,
        )

    def test_create_recipe_missing_optional_field_is_empty(self):
        response = self.verify_response_code(
            self.app.post(
                "/api/v1/recipes",
                json={
                    "name": "Marshmallows",
                    "ingredients": [{"amount": "all", "item": "marshmallow"},],
                    "instructions": ["mix"],
                    "recipe_type": RecipeType.Dessert,
                    "cooking_style": "",
                    "source": "",
                    "notes": [],
                    "tags": [],
                },
            ),
            201,
        )
        new_id = self.assertFieldIn(response, field="id")
        self.ids_to_cleanup.append(new_id)
        recipe = self.assertItemExists(new_id, item_type=Recipe)
        self.assertIsInstance(recipe, Recipe, f"Expected '{new_id}' to yield a Recipe!")
        assert isinstance(recipe, Recipe)  # Shouldn't have to do this...
        self.assertEqual(recipe.url, "", f"Expected the url to be empty, but was '{recipe.url}'")

    def test_create_recipe_missing_body(self):
        self.verify_response_code(self.app.post("/api/v1/recipes"), 400)

    # endregion

    # region Read
    def test_get_all_recipes(self):
        response = self.verify_response_code(self.app.get("/api/v1/recipes"), 200)
        recipes = self.assertFieldIn(response, field="recipes")
        self.assertEqual(len(recipes), 2, f"Expected 2 recipes in response -- {response}")

    def test_get_single_recipe(self):
        response = self.verify_response_code(
            self.app.get(f"/api/v1/recipes/{self.ids_to_cleanup[0]}"), 200
        )
        name = self.assertFieldIn(response, field="name")
        self.assertEqual(name, "Creme Fraiche", f"Unexpected name '{name}'")

    def test_get_single_nonexistent_recipe(self):
        self.verify_response_code(self.app.get("/api/v1/recipes/5f0113731c990801cc5d3240"), 404)

    # endregion

    # region Update
    def test_update_recipe(self):
        response = self.verify_response_code(
            self.app.put(
                f"/api/v1/recipes/{self.ids_to_cleanup[0]}",
                json={
                    "name": "Marshmallows",
                    "ingredients": [{"amount": "all", "item": "marshmallow"},],
                    "instructions": ["mix"],
                    "recipe_type": RecipeType.Dessert,
                    "cooking_style": "",
                    "url": self.test_recipes[0]["url"],
                    "source": "",
                    "notes": [],
                    "tags": [],
                },
            ),
            200,
        )
        name = self.assertFieldIn(response, field="name")
        self.assertEqual(name, "Marshmallows", "'name' field did not update correctly")
        url = self.assertFieldIn(response, field="url")
        self.assertEqual(
            url, self.test_recipes[0]["url"], "'url' field was updated but shouldn't have been"
        )

    def test_update_recipe_extra_field(self):
        self.verify_response_code(
            self.app.put(
                f"/api/v1/recipes/{self.ids_to_cleanup[0]}",
                json={
                    "name": "Marshmallows",
                    "ingredients": [{"amount": "all", "item": "marshmallow"},],
                    "instructions": ["mix"],
                    "recipe_type": RecipeType.Dessert,
                    "cooking_style": "",
                    "url": "",
                    "source": "",
                    "notes": [],
                    "foo": "bar",  # Extra field -- should throw error
                    "tags": [],
                },
            ),
            400,
        )

    def test_update_recipe_missing_required_field(self):
        self.verify_response_code(
            self.app.put(
                f"/api/v1/recipes/{self.ids_to_cleanup[0]}",
                json={
                    "ingredients": [{"amount": "all", "item": "marshmallow"},],
                    "instructions": ["mix"],
                    "recipe_type": RecipeType.Dessert,
                    "cooking_style": "",
                    "url": "",
                    "source": "",
                    "notes": [],
                    "tags": [],
                },
            ),
            400,
        )

    def test_update_recipe_missing_optional_field_is_empty(self):
        response = self.verify_response_code(
            self.app.put(
                f"/api/v1/recipes/{self.ids_to_cleanup[0]}",
                json={
                    "name": "Marshmallows",
                    "ingredients": [{"amount": "all", "item": "marshmallow"},],
                    "instructions": ["mix"],
                    "recipe_type": RecipeType.Dessert,
                    "cooking_style": "",
                    "source": "",
                    "notes": [],
                    "tags": [],
                },
            ),
            200,
        )
        name = self.assertFieldIn(response, field="name")
        self.assertEqual(name, "Marshmallows", "'name' field did not update correctly")
        url = self.assertFieldIn(response, field="url")
        self.assertEqual(url, "", f"Expected 'url' field to be empty but it was '{url}'")

    # endregion

    # region Delete
    def test_delete_recipe(self):
        with MongoConnector(Recipe, is_test=True) as db:
            new_id = db.create(
                Recipe.from_request(
                    {
                        "name": "Marshmallows",
                        "ingredients": [{"amount": "all", "item": "marshmallow"},],
                        "instructions": ["mix"],
                        "recipe_type": RecipeType.Dessert,
                        "cooking_style": "",
                        "url": "",
                        "source": "",
                        "notes": [],
                        "tags": [],
                    },
                )
            )
            self.ids_to_cleanup.append(new_id)
        response = self.verify_response_code(self.app.delete(f"/api/v1/recipes/{new_id}"), 204)
        self.assertEqual(response, {}, f"Expected empty response -- {response}")

    def test_delete_nonexistent_recipe(self):
        self.verify_response_code(self.app.delete("/api/v1/recipes/5f0113731c990801cc5d3240"), 404)

    # endregion
