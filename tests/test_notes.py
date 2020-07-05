from minerva import MongoConnector
from minerva.categories.notes import Note
from .test_categories_base import CategoriesTestsBase


class NotesTests(CategoriesTestsBase):
    def setUp(self) -> None:
        self.item_type = Note
        super().setUp()
        self.test_notes = [
            {"contents": "First Note", "url": "google.com", "tags": []},
            {"contents": "Second Note", "url": "ddg.com", "tags": []},
        ]
        with MongoConnector(Note, is_test=True) as db:
            for note in self.test_notes:
                self.ids_to_cleanup.append(db.create(Note.from_request(note)))

    def tearDown(self) -> None:
        super().tearDown()

    # region Create
    def test_create_note(self):
        response = self.verify_response_code(
            self.app.post(
                "/api/v1/notes",
                json={"contents": "TEST_CREATE_NOTE", "url": "speedrun.com", "tags": []},
            ),
            201,
        )
        new_id = self.assertFieldIn(response, field="id")
        self.ids_to_cleanup.append(new_id)

    def text_create_note_missing_required_field(self):
        self.verify_response_code(
            self.app.post("/api/v1/notes", json={"url": "speedrun.com", "tags": []}), 404
        )

    def test_create_note_missing_optional_field_is_empty(self):
        response = self.verify_response_code(
            self.app.post(
                "/api/v1/notes", json={"contents": "TEST_CREATE_NOTE_MISSING_URL", "tags": []}
            ),
            201,
        )
        new_id = self.assertFieldIn(response, field="id")
        self.ids_to_cleanup.append(new_id)
        note = self.assertItemExists(new_id, item_type=Note)
        self.assertIsInstance(note, Note, f"Expected '{new_id}' to yield a Note!")
        assert isinstance(note, Note)  # Shouldn't have to do this...
        self.assertEqual(note.url, "", f"Expected the url to be empty, but was '{note.url}'")

    def test_create_note_missing_body(self):
        self.verify_response_code(self.app.post("/api/v1/notes"), 400)

    # endregion

    # region Read
    def test_get_all_notes(self):
        response = self.verify_response_code(self.app.get("/api/v1/notes"), 200)
        notes = self.assertFieldIn(response, field="notes")
        self.assertEqual(len(notes), 2, f"Expected 2 notes in response -- {response}")

    def test_get_single_note(self):
        response = self.verify_response_code(
            self.app.get(f"/api/v1/notes/{self.ids_to_cleanup[0]}"), 200
        )
        contents = self.assertFieldIn(response, field="contents")
        self.assertEqual(contents, "First Note", f"Unexpected contents '{contents}'")

    def test_get_single_nonexistent_note(self):
        self.verify_response_code(self.app.get("/api/v1/notes/5f0113731c990801cc5d3240"), 404)

    # endregion

    # region Update
    def test_update_note(self):
        response = self.verify_response_code(
            self.app.put(
                f"/api/v1/notes/{self.ids_to_cleanup[0]}",
                json={
                    "contents": "New First Contents",
                    "url": self.test_notes[0]["url"],
                    "tags": [],
                },
            ),
            200,
        )
        contents = self.assertFieldIn(response, field="contents")
        self.assertEqual(
            contents, "New First Contents", "'contents' field did not update correctly"
        )
        url = self.assertFieldIn(response, field="url")
        self.assertEqual(
            url, self.test_notes[0]["url"], "'url' field was updated but shouldn't have been"
        )

    def test_update_note_extra_field(self):
        self.verify_response_code(
            self.app.put(
                f"/api/v1/notes/{self.ids_to_cleanup[0]}",
                json={
                    "contents": "Update with extra fields",
                    "url": self.test_notes[0]["url"],
                    "tags": [],
                    "foo": "bar",  # Extra field -- should throw error
                },
            ),
            400,
        )

    def test_update_note_missing_required_field(self):
        self.verify_response_code(
            self.app.put(
                f"/api/v1/notes/{self.ids_to_cleanup[0]}",
                json={"url": self.test_notes[0]["url"], "tags": []},
            ),
            400,
        )

    def test_update_note_missing_optional_field_is_empty(self):
        response = self.verify_response_code(
            self.app.put(
                f"/api/v1/notes/{self.ids_to_cleanup[0]}",
                json={"contents": "Update with extra fields", "tags": []},
            ),
            200,
        )
        contents = self.assertFieldIn(response, field="contents")
        self.assertEqual(
            contents, "Update with extra fields", "'contents' field did not update correctly"
        )
        url = self.assertFieldIn(response, field="url")
        self.assertEqual(url, "", f"Expected 'url' field to be empty but it was '{url}'")

    # endregion

    # region Delete
    def test_delete_note(self):
        with MongoConnector(Note, is_test=True) as db:
            new_id = db.create(
                Note.from_request({"contents": "TEST_DELETE_NOTE", "url": "", "tags": []})
            )
            self.ids_to_cleanup.append(new_id)
        response = self.verify_response_code(self.app.delete(f"/api/v1/notes/{new_id}"), 204)
        self.assertEqual(response, {}, f"Expected empty response -- {response}")

    def test_delete_nonexistent_note(self):
        self.verify_response_code(self.app.delete("/api/v1/notes/5f0113731c990801cc5d3240"), 404)

    # endregion
