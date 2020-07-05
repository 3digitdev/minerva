from minerva import MongoConnector
from minerva.categories.employments import Employment
from .test_categories_base import CategoriesTestsBase


class EmploymentsTests(CategoriesTestsBase):
    def setUp(self) -> None:
        self.item_type = Employment
        super().setUp()
        self.test_employments = [
            {
                "title": "Senior Intern",
                "salary": "1",
                "employer": {
                    "address": {
                        "number": "123",
                        "street": "Main St",
                        "extra": "APT 456",
                        "city": "Nowhere",
                        "state": "NE",
                        "zip_code": "98765",
                    },
                    "phone": "+12345678900",
                    "supervisor": "Santa",
                },
                "tags": [],
            },
            {
                "title": "Junior Intern",
                "salary": "2",
                "employer": {
                    "address": {
                        "number": "456",
                        "street": "Main St",
                        "extra": "",
                        "city": "Nowhere",
                        "state": "NE",
                        "zip_code": "98765",
                    },
                    "phone": "+12345678900",
                    "supervisor": "",
                },
                "tags": [],
            },
        ]
        with MongoConnector(Employment, is_test=True) as db:
            for employment in self.test_employments:
                self.ids_to_cleanup.append(db.create(Employment.from_request(employment)))

    def tearDown(self) -> None:
        super().tearDown()

    # region Create
    def test_create_employment(self):
        response = self.verify_response_code(
            self.app.post(
                "/api/v1/employment",
                json={
                    "title": "Senior Intern",
                    "salary": "1",
                    "employer": {
                        "address": {
                            "number": "123",
                            "street": "Main St",
                            "extra": "APT 456",
                            "city": "Nowhere",
                            "state": "NE",
                            "zip_code": "98765",
                        },
                        "phone": "+12345678900",
                        "supervisor": "Santa",
                    },
                    "tags": [],
                },
            ),
            201,
        )
        new_id = self.assertFieldIn(response, field="id")
        self.ids_to_cleanup.append(new_id)

    def text_create_employment_missing_required_field(self):
        self.verify_response_code(
            self.app.post(
                "/api/v1/employment",
                json={
                    "salary": "1",
                    "employer": {
                        "address": {
                            "number": "123",
                            "street": "Main St",
                            "extra": "APT 456",
                            "city": "Nowhere",
                            "state": "NE",
                            "zip_code": "98765",
                        },
                        "phone": "+12345678900",
                        "supervisor": "Santa",
                    },
                    "tags": [],
                },
            ),
            404,
        )

    def test_create_employment_missing_optional_field_is_empty(self):
        response = self.verify_response_code(
            self.app.post(
                "/api/v1/employment",
                json={
                    "title": "Senior Intern",
                    "salary": "1",
                    "employer": {
                        "address": {
                            "number": "123",
                            "street": "Main St",
                            "extra": "APT 456",
                            "city": "Nowhere",
                            "state": "NE",
                            "zip_code": "98765",
                        },
                        "phone": "+12345678900",
                    },
                    "tags": [],
                },
            ),
            201,
        )
        new_id = self.assertFieldIn(response, field="id")
        self.ids_to_cleanup.append(new_id)
        employment = self.assertItemExists(new_id, item_type=Employment)
        self.assertIsInstance(employment, Employment, f"Expected '{new_id}' to yield a Employment!")
        assert isinstance(employment, Employment)  # Shouldn't have to do this...
        self.assertEqual(
            employment.employer.supervisor,
            "",
            f"Expected the employer/supervisor to be empty, but was '{employment.employer.supervisor}'",
        )

    def test_create_employment_missing_body(self):
        self.verify_response_code(self.app.post("/api/v1/employment"), 400)

    # endregion

    # region Read
    def test_get_all_employments(self):
        response = self.verify_response_code(self.app.get("/api/v1/employment"), 200)
        employments = self.assertFieldIn(response, field="employments")
        self.assertEqual(len(employments), 2, f"Expected 2 employments in response -- {response}")

    def test_get_single_employment(self):
        response = self.verify_response_code(
            self.app.get(f"/api/v1/employment/{self.ids_to_cleanup[0]}"), 200
        )
        title = self.assertFieldIn(response, field="title")
        self.assertEqual(title, "Senior Intern", f"Unexpected title '{title}")

    def test_get_single_nonexistent_employment(self):
        self.verify_response_code(self.app.get("/api/v1/employment/5f0113731c990801cc5d3240"), 404)

    # endregion

    # region Update
    def test_update_employment(self):
        response = self.verify_response_code(
            self.app.put(
                f"/api/v1/employment/{self.ids_to_cleanup[0]}",
                json={
                    "title": "Junior Intern",
                    "salary": self.test_employments[0]["salary"],
                    "employer": {
                        "address": {
                            "number": "123",
                            "street": "Main St",
                            "extra": "APT 456",
                            "city": "Nowhere",
                            "state": "NE",
                            "zip_code": "98765",
                        },
                        "phone": "+12345678900",
                        "supervisor": "Santa",
                    },
                    "tags": [],
                },
            ),
            200,
        )
        title = self.assertFieldIn(response, field="title")
        self.assertEqual(title, "Junior Intern", "'title' field did not update correctly")
        salary = self.assertFieldIn(response, field="salary")
        self.assertEqual(
            salary,
            self.test_employments[0]["salary"],
            "'salary' field was updated but shouldn't have been",
        )

    def test_update_employment_extra_field(self):
        # TODO:  Right now this test is tuned to pass and ignore the field.
        #        I want to eventually get this so it errors if there's unexpected fields.
        response = self.verify_response_code(
            self.app.put(
                f"/api/v1/employment/{self.ids_to_cleanup[0]}",
                json={
                    "title": "Junior Intern",
                    "salary": "1",
                    "employer": {
                        "address": {
                            "number": "123",
                            "street": "Main St",
                            "extra": "APT 456",
                            "city": "Nowhere",
                            "state": "NE",
                            "zip_code": "98765",
                        },
                        "phone": "+12345678900",
                        "supervisor": "Santa",
                    },
                    "foo": "bar",
                    "tags": [],
                },
            ),
            200,
        )
        title = self.assertFieldIn(response, field="title")
        self.assertEqual(title, "Junior Intern", "'title' field did not update correctly")
        self.assertNotIn(
            "foo", response, f"Expected 'foo' field to not be in response body -- {response}"
        )

    def test_update_employment_missing_required_field(self):
        self.verify_response_code(
            self.app.put(
                f"/api/v1/employment/{self.ids_to_cleanup[0]}",
                json={
                    "salary": "1",
                    "employer": {
                        "address": {
                            "number": "123",
                            "street": "Main St",
                            "extra": "APT 456",
                            "city": "Nowhere",
                            "state": "NE",
                            "zip_code": "98765",
                        },
                        "phone": "+12345678900",
                        "supervisor": "Santa",
                    },
                    "tags": [],
                },
            ),
            400,
        )

    def test_update_employment_missing_optional_field_is_empty(self):
        response = self.verify_response_code(
            self.app.put(
                f"/api/v1/employment/{self.ids_to_cleanup[0]}",
                json={
                    "title": "Junior Intern",
                    "salary": "1",
                    "employer": {
                        "address": {
                            "number": "123",
                            "street": "Main St",
                            "extra": "APT 456",
                            "city": "Nowhere",
                            "state": "NE",
                            "zip_code": "98765",
                        },
                        "phone": "+12345678900",
                    },
                    "tags": [],
                },
            ),
            200,
        )
        title = self.assertFieldIn(response, field="title")
        self.assertEqual(title, "Junior Intern", "'title' field did not update correctly")
        employer = self.assertFieldIn(response, field="employer")
        self.assertEqual(
            employer["supervisor"],
            "",
            f"Expected 'supervisor' field in 'employer' to be empty but it was '{employer['supervisor']}'",
        )

    # endregion

    # region Delete
    def test_delete_employment(self):
        with MongoConnector(Employment, is_test=True) as db:
            new_id = db.create(
                Employment.from_request(
                    {
                        "title": "Test Delete Employment",
                        "salary": "1",
                        "employer": {
                            "address": {
                                "number": "123",
                                "street": "Main St",
                                "extra": "APT 456",
                                "city": "Nowhere",
                                "state": "NE",
                                "zip_code": "98765",
                            },
                            "phone": "+12345678900",
                            "supervisor": "",
                        },
                        "tags": [],
                    }
                )
            )
            self.ids_to_cleanup.append(new_id)
        response = self.verify_response_code(self.app.delete(f"/api/v1/employment/{new_id}"), 204)
        self.assertEqual(response, {}, f"Expected empty response -- {response}")

    def test_delete_nonexistent_employment(self):
        self.verify_response_code(
            self.app.delete("/api/v1/employment/5f0113731c990801cc5d3240"), 404
        )

    # endregion
