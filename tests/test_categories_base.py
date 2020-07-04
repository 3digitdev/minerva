import unittest

from minerva import create_app


# Base method for testing all the routes --
# Helps avoid having to rebuild the Flask app in each test file
class CategoriesTestsBase(unittest.TestCase):
    def setUp(self) -> None:
        app = create_app({"TESTING": True, "DEBUG": False})
        self.app = app.test_client()

    def tearDown(self) -> None:
        pass
