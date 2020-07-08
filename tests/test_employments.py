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
                "start_month": "1",
                "start_year": "2015",
                "end_month": "2",
                "end_year": "2019",
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
                "start_month": "1",
                "start_year": "2015",
                "end_month": "",
                "end_year": "",
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
                "/api/v1/employments",
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
                    "start_month": "1",
                    "start_year": "2015",
                    "end_month": "",
                    "end_year": "",
                    "tags": [],
                },
            ),
            201,
        )
        new_id = self.assertFieldIn(response, field="id")
        self.ids_to_cleanup.append(new_id)

    def test_create_employment_missing_required_field(self):
        self.verify_response_code(
            self.app.post(
                "/api/v1/employments",
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
                    "start_month": "1",
                    "start_year": "2015",
                    "end_month": "",
                    "end_year": "",
                    "tags": [],
                },
            ),
            400,
        )

    def test_create_employment_missing_optional_field_is_empty(self):
        response = self.verify_response_code(
            self.app.post(
                "/api/v1/employments",
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
                    "start_month": "1",
                    "start_year": "2015",
                    "end_month": "",
                    "end_year": "",
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
        self.verify_response_code(self.app.post("/api/v1/employments"), 400)

    # endregion

    # region Read
    def test_get_all_employments(self):
        response = self.verify_response_code(self.app.get("/api/v1/employments"), 200)
        employments = self.assertFieldIn(response, field="employments")
        self.assertEqual(len(employments), 2, f"Expected 2 employments in response -- {response}")

    def test_get_all_employments_paginated(self):
        response = self.verify_response_code(
            self.app.get("/api/v1/employments?page=2&count=1"), 200
        )
        employments = self.assertFieldIn(response, field="employments")
        self.assertEqual(
            len(employments), 1, f"Expected just 1 employment in response -- {response}"
        )

    def test_get_single_employment(self):
        response = self.verify_response_code(
            self.app.get(f"/api/v1/employments/{self.ids_to_cleanup[0]}"), 200
        )
        title = self.assertFieldIn(response, field="title")
        self.assertEqual(title, "Senior Intern", f"Unexpected title '{title}'")

    def test_get_single_nonexistent_employment(self):
        self.verify_response_code(self.app.get("/api/v1/employments/5f0113731c990801cc5d3240"), 404)

    # endregion

    # region Update
    def test_update_employment(self):
        response = self.verify_response_code(
            self.app.put(
                f"/api/v1/employments/{self.ids_to_cleanup[0]}",
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
                    "start_month": "1",
                    "start_year": "2015",
                    "end_month": "",
                    "end_year": "",
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
        self.verify_response_code(
            self.app.put(
                f"/api/v1/employments/{self.ids_to_cleanup[0]}",
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
                    "start_month": "1",
                    "start_year": "2015",
                    "end_month": "",
                    "end_year": "",
                    "foo": "bar",  # Extra field, should throw error
                    "tags": [],
                },
            ),
            400,
        )

    def test_update_employment_missing_required_field(self):
        self.verify_response_code(
            self.app.put(
                f"/api/v1/employments/{self.ids_to_cleanup[0]}",
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
                    "start_month": "1",
                    "start_year": "2015",
                    "end_month": "",
                    "end_year": "",
                    "tags": [],
                },
            ),
            400,
        )

    def test_update_employment_missing_optional_field_is_empty(self):
        response = self.verify_response_code(
            self.app.put(
                f"/api/v1/employments/{self.ids_to_cleanup[0]}",
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
                    "start_month": "1",
                    "start_year": "2015",
                    "end_month": "",
                    "end_year": "",
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
                        "start_month": "1",
                        "start_year": "2015",
                        "end_month": "",
                        "end_year": "",
                        "tags": [],
                    }
                )
            )
            self.ids_to_cleanup.append(new_id)
        response = self.verify_response_code(self.app.delete(f"/api/v1/employments/{new_id}"), 204)
        self.assertEqual(response, {}, f"Expected empty response -- {response}")

    def test_delete_nonexistent_employment(self):
        self.verify_response_code(
            self.app.delete("/api/v1/employments/5f0113731c990801cc5d3240"), 404
        )

    # endregion
