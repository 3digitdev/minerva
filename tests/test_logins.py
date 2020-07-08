from minerva import MongoConnector
from minerva.categories.logins import Login
from .test_categories_base import CategoriesTestsBase


class LoginsTests(CategoriesTestsBase):
    def setUp(self) -> None:
        self.item_type = Login
        super().setUp()
        self.test_logins = [
            {
                "application": "First App",
                "password": "foobar",
                "url": "google.com",
                "username": "foo",
                "email": "foo@bar.com",
                "security_questions": [{"question": "Who?", "answer": "Me"}],
                "tags": [],
            },
            {
                "application": "Second App",
                "password": "bazbat",
                "url": "",
                "username": "",
                "email": "",
                "security_questions": [],
                "tags": [],
            },
        ]
        with MongoConnector(Login, is_test=True) as db:
            for login in self.test_logins:
                self.ids_to_cleanup.append(db.create(Login.from_request(login)))

    def tearDown(self) -> None:
        super().tearDown()

    # region Create
    def test_create_login(self):
        response = self.verify_response_code(
            self.app.post(
                "/api/v1/logins",
                json={
                    "application": "New App",
                    "password": "lorem ipsum",
                    "url": "",
                    "username": "",
                    "email": "",
                    "security_questions": [],
                    "tags": [],
                },
            ),
            201,
        )
        new_id = self.assertFieldIn(response, field="id")
        self.ids_to_cleanup.append(new_id)

    def test_create_login_missing_required_field(self):
        self.verify_response_code(
            self.app.post(
                "/api/v1/logins",
                json={
                    "password": "bazbat",
                    "url": "",
                    "username": "",
                    "email": "",
                    "security_questions": [],
                    "tags": [],
                },
            ),
            400,
        )

    def test_create_login_missing_optional_field_is_empty(self):
        response = self.verify_response_code(
            self.app.post(
                "/api/v1/logins",
                json={
                    "application": "Second App",
                    "password": "bazbat",
                    "username": "",
                    "email": "",
                    "security_questions": [],
                    "tags": [],
                },
            ),
            201,
        )
        new_id = self.assertFieldIn(response, field="id")
        self.ids_to_cleanup.append(new_id)
        login = self.assertItemExists(new_id, item_type=Login)
        self.assertIsInstance(login, Login, f"Expected '{new_id}' to yield a Login!")
        assert isinstance(login, Login)  # Shouldn't have to do this...
        self.assertEqual(login.url, "", f"Expected the url to be empty, but was '{login.url}'")

    def test_create_login_missing_body(self):
        self.verify_response_code(self.app.post("/api/v1/logins"), 400)

    # endregion

    # region Read
    def test_get_all_logins(self):
        response = self.verify_response_code(self.app.get("/api/v1/logins"), 200)
        logins = self.assertFieldIn(response, field="logins")
        self.assertEqual(len(logins), 2, f"Expected 2 logins in response -- {response}")

    def test_get_all_logins_paginated(self):
        response = self.verify_response_code(self.app.get("/api/v1/logins?page=2&count=1"), 200)
        logins = self.assertFieldIn(response, field="logins")
        self.assertEqual(len(logins), 1, f"Expected just 1 login in response -- {response}")

    def test_get_single_login(self):
        response = self.verify_response_code(
            self.app.get(f"/api/v1/logins/{self.ids_to_cleanup[0]}"), 200
        )
        application = self.assertFieldIn(response, field="application")
        self.assertEqual(application, "First App", f"Unexpected application '{application}'")

    def test_get_single_nonexistent_login(self):
        self.verify_response_code(self.app.get("/api/v1/logins/5f0113731c990801cc5d3240"), 404)

    # endregion

    # region Update
    def test_update_login(self):
        response = self.verify_response_code(
            self.app.put(
                f"/api/v1/logins/{self.ids_to_cleanup[0]}",
                json={
                    "application": "Updated App",
                    "password": "bloo blah",
                    "url": self.test_logins[0]["url"],
                    "username": "carl",
                    "email": "carl@lang.com",
                    "security_questions": [],
                    "tags": [],
                },
            ),
            200,
        )
        application = self.assertFieldIn(response, field="application")
        self.assertEqual(application, "Updated App", "'application' field did not update correctly")
        url = self.assertFieldIn(response, field="url")
        self.assertEqual(
            url, self.test_logins[0]["url"], "'url' field was updated but shouldn't have been"
        )

    def test_update_login_extra_field(self):
        self.verify_response_code(
            self.app.put(
                f"/api/v1/logins/{self.ids_to_cleanup[0]}",
                json={
                    "application": "Update with extra fields",
                    "password": self.test_logins[0]["password"],
                    "url": self.test_logins[0]["url"],
                    "username": self.test_logins[0]["username"],
                    "email": self.test_logins[0]["email"],
                    "security_questions": self.test_logins[0]["security_questions"],
                    "foo": "bar",  # Extra field -- should throw error
                    "tags": self.test_logins[0]["tags"],
                },
            ),
            400,
        )

    def test_update_login_missing_required_field(self):
        self.verify_response_code(
            self.app.put(
                f"/api/v1/logins/{self.ids_to_cleanup[0]}",
                json={
                    "password": "malbolge",
                    "url": self.test_logins[0]["url"],
                    "username": self.test_logins[0]["username"],
                    "email": self.test_logins[0]["email"],
                    "security_questions": self.test_logins[0]["security_questions"],
                    "tags": self.test_logins[0]["tags"],
                },
            ),
            400,
        )

    def test_update_login_missing_optional_field_is_empty(self):
        response = self.verify_response_code(
            self.app.put(
                f"/api/v1/logins/{self.ids_to_cleanup[0]}",
                json={
                    "application": "Second App Updated",
                    "password": self.test_logins[0]["password"],
                    "username": self.test_logins[0]["username"],
                    "email": self.test_logins[0]["email"],
                    "security_questions": self.test_logins[0]["security_questions"],
                    "tags": self.test_logins[0]["tags"],
                },
            ),
            200,
        )
        application = self.assertFieldIn(response, field="application")
        self.assertEqual(
            application, "Second App Updated", "'application' field did not update correctly"
        )
        url = self.assertFieldIn(response, field="url")
        self.assertEqual(url, "", f"Expected 'url' field to be empty but it was '{url}'")

    # endregion

    # region Delete
    def test_delete_login(self):
        with MongoConnector(Login, is_test=True) as db:
            new_id = db.create(
                Login.from_request(
                    {
                        "application": "Second App",
                        "password": "malbolge",
                        "url": "",
                        "username": "",
                        "email": "",
                        "security_questions": [],
                        "tags": [],
                    }
                )
            )
            self.ids_to_cleanup.append(new_id)
        response = self.verify_response_code(self.app.delete(f"/api/v1/logins/{new_id}"), 204)
        self.assertEqual(response, {}, f"Expected empty response -- {response}")

    def test_delete_nonexistent_login(self):
        self.verify_response_code(self.app.delete("/api/v1/logins/5f0113731c990801cc5d3240"), 404)

    # endregion
