from minerva.categories.tags import Tag
from .test_categories_base import CategoriesTestsBase


class TagsTests(CategoriesTestsBase):
    def setUp(self) -> None:
        self.item_type = Tag
        super().setUp()
        self.test_tags = [{"name": "First"}, {"name": "Second"}]
        with self.datastore(Tag, config=self.config) as db:
            for tag in self.test_tags:
                self.ids_to_cleanup.append(db.create(Tag.from_request(tag)))

    def tearDown(self) -> None:
        super().tearDown()

    # region Create
    def test_create_tag(self):
        response = self.verify_response_code(
            self.app.post("/api/v1/tags", json={"name": "New"}), 201,
        )
        new_id = self.assertFieldIn(response, field="id")
        self.ids_to_cleanup.append(new_id)

    def test_create_tag_missing_required_field(self):
        self.verify_response_code(self.app.post("/api/v1/tags", json={}), 400)

    def test_create_tag_missing_body(self):
        self.verify_response_code(self.app.post("/api/v1/tags"), 400)

    # endregion

    # region Read
    def test_get_all_tags(self):
        response = self.verify_response_code(self.app.get("/api/v1/tags"), 200)
        tags = self.assertFieldIn(response, field="tags")
        self.assertEqual(len(tags), 2, f"Expected 2 tags in response -- {response}")

    def test_get_all_tags_paginated(self):
        response = self.verify_response_code(self.app.get("/api/v1/tags?page=2&count=1"), 200)
        tags = self.assertFieldIn(response, field="tags")
        self.assertEqual(len(tags), 1, f"Expected just 1 tag in response -- {response}")

    def test_get_single_tag(self):
        response = self.verify_response_code(
            self.app.get(f"/api/v1/tags/{self.ids_to_cleanup[0]}"), 200
        )
        name = self.assertFieldIn(response, field="name")
        self.assertEqual(name, "First", f"Unexpected name '{name}'")

    def test_get_single_nonexistent_tag(self):
        self.verify_response_code(self.app.get("/api/v1/tags/5f0113731c990801cc5d3240"), 404)

    # endregion

    # region Update
    def test_update_tag(self):
        response = self.verify_response_code(
            self.app.put(f"/api/v1/tags/{self.ids_to_cleanup[0]}", json={"name": "Updates"},), 200,
        )
        name = self.assertFieldIn(response, field="name")
        self.assertEqual(name, "Updates", "'name' field did not update correctly")

    def test_update_tag_extra_field(self):
        self.verify_response_code(
            self.app.put(
                f"/api/v1/tags/{self.ids_to_cleanup[0]}",
                json={"name": "Update", "foo": "bar",},  # Extra field -- should throw error
            ),
            400,
        )

    def test_update_tag_missing_required_field(self):
        self.verify_response_code(
            self.app.put(f"/api/v1/tags/{self.ids_to_cleanup[0]}", json={},), 400,
        )

    # endregion

    # region Delete
    def test_delete_tag(self):
        with self.datastore(Tag, config=self.config) as db:
            new_id = db.create(Tag.from_request({"name": "TEST_DELETE_TAG"}))
            self.ids_to_cleanup.append(new_id)
        response = self.verify_response_code(self.app.delete(f"/api/v1/tags/{new_id}"), 204)
        self.assertEqual(response, {}, f"Expected empty response -- {response}")

    def test_delete_nonexistent_tag(self):
        self.verify_response_code(self.app.delete("/api/v1/tags/5f0113731c990801cc5d3240"), 404)

    # endregion
