import mongomock

from .test_categories_base import CategoriesTestsBase


class NotesTests(CategoriesTestsBase):
    @mongomock.patch(servers=(("localhost", 27017),))
    def setUp(self) -> None:
        super().setUp()

    def tearDown(self) -> None:
        super().tearDown()

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_get_all_notes(self):
        response = self.app.get("/api/v1/notes")
        self.assertEqual(
            response.status_code,
            200,
            f"Expected 200 status code, got {response.status_code} -- {response.json}",
        )
        self.assertIn(
            "notes", response.json, f"Expected 'notes' to be in response body -- {response.json}"
        )
