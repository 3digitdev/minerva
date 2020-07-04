import unittest
from typing import Type

from flask import Response
from werkzeug.exceptions import BadRequest

from helpers.types import Maybe, JsonData
from minerva import create_app, Category, MongoConnector


# Base method for testing all the routes --
# Helps avoid having to rebuild the Flask app in each test file
class CategoriesTestsBase(unittest.TestCase):
    item_type: Maybe[Type[Category]]

    def setUp(self) -> None:
        app = create_app({"TESTING": True, "DEBUG": False})
        self.app = app.test_client()
        self.assertIsNotNone(
            self.item_type, "You forgot to instantiate the item type before calling the parent init"
        )
        self.ids_to_cleanup = []

    def tearDown(self) -> None:
        with MongoConnector(self.item_type, is_test=True) as db:
            for item_id in self.ids_to_cleanup:
                db.delete_one(item_id)

    # --- Helpers to save typing --- #
    def verify_response_code(self, response: Response, expected: int = 200):
        # If the response body is empty, this is needed
        try:
            body = response.json
        except BadRequest:
            body = {}
        self.assertEqual(
            response.status_code,
            expected,
            f"Expected {expected} status code, but got {response.status_code} -- {body}",
        )
        return body

    def assertFieldIn(self, response: JsonData, *, field: str):
        self.assertIn(field, response, f"Expected '{field}' field in response body -- {response}")
        return response[field]
