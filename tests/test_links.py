from minerva import MongoConnector
from minerva.categories.links import Link
from .test_categories_base import CategoriesTestsBase


class LinksTests(CategoriesTestsBase):
    def setUp(self) -> None:
        self.item_type = Link
        super().setUp()
        self.test_links = [
            {"name": "First Link", "url": "google.com", "notes": ["a", "b", "c"], "tags": []},
            {"name": "Second Link", "url": "ddg.com", "notes": [], "tags": []},
        ]
        with MongoConnector(Link, is_test=True) as db:
            for link in self.test_links:
                self.ids_to_cleanup.append(db.create(Link.from_request(link)))

    def tearDown(self) -> None:
        super().tearDown()

    # region Create
    def test_create_link(self):
        response = self.verify_response_code(
            self.app.post(
                "/api/v1/links",
                json={
                    "name": "TEST_CREATE_NOTE",
                    "url": "speedrun.com",
                    "notes": ["a", "b"],
                    "tags": [],
                },
            ),
            201,
        )
        new_id = self.assertFieldIn(response, field="id")
        self.ids_to_cleanup.append(new_id)

    def text_create_link_missing_required_field(self):
        self.verify_response_code(
            self.app.post("/api/v1/links", json={"url": "speedrun.com", "tags": []}), 404
        )

    def test_create_link_missing_optional_field_is_empty(self):
        response = self.verify_response_code(
            self.app.post(
                "/api/v1/links",
                json={"name": "TEST_CREATE_LINK_MISSING_NOTES", "url": "speedrun.com", "tags": []},
            ),
            201,
        )
        new_id = self.assertFieldIn(response, field="id")
        self.ids_to_cleanup.append(new_id)
        link = self.assertItemExists(new_id, item_type=Link)
        self.assertIsInstance(link, Link, f"Expected '{new_id}' to yield a Link!")
        assert isinstance(link, Link)  # Shouldn't have to do this...
        self.assertEqual(
            link.notes, [], f"Expected the 'notes' to be empty, but was '{link.notes}'"
        )

    def test_create_link_missing_body(self):
        self.verify_response_code(self.app.post("/api/v1/links"), 400)

    # endregion

    # region Read
    def test_get_all_links(self):
        response = self.verify_response_code(self.app.get("/api/v1/links"), 200)
        links = self.assertFieldIn(response, field="links")
        self.assertEqual(len(links), 2, f"Expected 2 links in response -- {response}")

    def test_get_single_link(self):
        response = self.verify_response_code(
            self.app.get(f"/api/v1/links/{self.ids_to_cleanup[0]}"), 200
        )
        name = self.assertFieldIn(response, field="name")
        self.assertEqual(name, "First Link", f"Unexpected contents '{name}'")

    def test_get_single_nonexistent_link(self):
        self.verify_response_code(self.app.get("/api/v1/links/5f0113731c990801cc5d3240"), 404)

    # endregion

    # region Update
    def test_update_link(self):
        response = self.verify_response_code(
            self.app.put(
                f"/api/v1/links/{self.ids_to_cleanup[0]}",
                json={
                    "name": "New First Name",
                    "url": self.test_links[0]["url"],
                    "notes": self.test_links[0]["notes"],
                    "tags": [],
                },
            ),
            200,
        )
        name = self.assertFieldIn(response, field="name")
        self.assertEqual(name, "New First Name", "'name' field did not update correctly")
        url = self.assertFieldIn(response, field="url")
        self.assertEqual(
            url, self.test_links[0]["url"], "'url' field was updated but shouldn't have been"
        )

    def test_update_link_extra_field(self):
        self.verify_response_code(
            self.app.put(
                f"/api/v1/links/{self.ids_to_cleanup[0]}",
                json={
                    "name": "Update with extra fields",
                    "url": self.test_links[0]["url"],
                    "notes": [],
                    "tags": [],
                    "foo": "bar",  # Extra field -- should throw error
                },
            ),
            400,
        )

    def test_update_link_missing_required_field(self):
        self.verify_response_code(
            self.app.put(
                f"/api/v1/links/{self.ids_to_cleanup[0]}",
                json={"url": self.test_links[0]["url"], "tags": []},
            ),
            400,
        )

    def test_update_link_missing_optional_field_is_empty(self):
        response = self.verify_response_code(
            self.app.put(
                f"/api/v1/links/{self.ids_to_cleanup[0]}",
                json={"name": "Update with extra fields", "url": "speedrun.com", "tags": [],},
            ),
            200,
        )
        name = self.assertFieldIn(response, field="name")
        self.assertEqual(name, "Update with extra fields", "'name' field did not update correctly")
        notes = self.assertFieldIn(response, field="notes")
        self.assertEqual(notes, [], f"Expected 'notes' field to be empty but it was '{notes}'")

    # endregion

    # region Delete
    def test_delete_link(self):
        with MongoConnector(Link, is_test=True) as db:
            new_id = db.create(
                Link.from_request({"name": "TEST_DELETE_NOTE", "url": "", "notes": [], "tags": []})
            )
            self.ids_to_cleanup.append(new_id)
        response = self.verify_response_code(self.app.delete(f"/api/v1/links/{new_id}"), 204)
        self.assertEqual(response, {}, f"Expected empty response -- {response}")

    def test_delete_nonexistent_link(self):
        self.verify_response_code(self.app.delete("/api/v1/links/5f0113731c990801cc5d3240"), 404)

    # endregion
