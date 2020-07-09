from minerva.categories.housings import Housing
from .test_categories_base import CategoriesTestsBase


class HousingsTests(CategoriesTestsBase):
    def setUp(self) -> None:
        self.item_type = Housing
        super().setUp()
        self.test_housings = [
            {
                "address": {
                    "number": "123",
                    "street": "Main St",
                    "extra": "APT 456",
                    "city": "Nowhere",
                    "state": "NE",
                    "zip_code": "98765",
                },
                "start_month": "1",
                "start_year": "2020",
                "end_month": "5",
                "end_year": "2020",
                "monthly_payment": 1545,
                "tags": [],
            },
            {
                "address": {
                    "number": "123",
                    "street": "Main St",
                    "extra": "",
                    "city": "Nowhere",
                    "state": "NE",
                    "zip_code": "98765",
                },
                "start_month": "1",
                "start_year": "2020",
                "end_month": "",
                "end_year": "",
                "monthly_payment": 0,
                "tags": [],
            },
        ]
        with self.datastore(Housing, config=self.config) as db:
            for housing in self.test_housings:
                self.ids_to_cleanup.append(db.create(Housing.from_request(housing)))

    def tearDown(self) -> None:
        super().tearDown()

    # region Create
    def test_create_housing(self):
        response = self.verify_response_code(
            self.app.post(
                "/api/v1/housings",
                json={
                    "address": {
                        "number": "123",
                        "street": "Main St",
                        "extra": "APT 456",
                        "city": "Nowhere",
                        "state": "NE",
                        "zip_code": "98765",
                    },
                    "start_month": "1",
                    "start_year": "2020",
                    "end_month": "5",
                    "end_year": "2020",
                    "monthly_payment": 1545,
                    "tags": [],
                },
            ),
            201,
        )
        new_id = self.assertFieldIn(response, field="id")
        self.ids_to_cleanup.append(new_id)

    def test_create_housing_missing_required_field(self):
        self.verify_response_code(
            self.app.post(
                "/api/v1/housings",
                json={
                    "address": {
                        "number": "123",
                        "street": "Main St",
                        "extra": "APT 456",
                        "city": "Nowhere",
                        "state": "NE",
                        "zip_code": "98765",
                        "tags": [],
                    },
                    "start_year": "2020",
                    "end_month": "5",
                    "end_year": "2020",
                    "monthly_payment": 1545,
                    "tags": [],
                },
            ),
            400,
        )

    def test_create_housing_missing_optional_field_is_empty(self):
        response = self.verify_response_code(
            self.app.post(
                "/api/v1/housings",
                json={
                    "address": {
                        "number": "123",
                        "street": "Main St",
                        "extra": "APT 456",
                        "city": "Nowhere",
                        "state": "NE",
                        "zip_code": "98765",
                    },
                    "start_month": "1",
                    "start_year": "2020",
                    "end_year": "2020",
                    "monthly_payment": 1545,
                    "tags": [],
                },
            ),
            201,
        )
        new_id = self.assertFieldIn(response, field="id")
        self.ids_to_cleanup.append(new_id)
        housing = self.assertItemExists(new_id, item_type=Housing)
        self.assertIsInstance(housing, Housing, f"Expected '{new_id}' to yield a Housing!")
        assert isinstance(housing, Housing)  # Shouldn't have to do this...
        self.assertEqual(
            housing.end_month,
            "",
            f"Expected the 'end_month' to be empty, but was '{housing.end_month}'",
        )

    def test_create_housing_missing_body(self):
        self.verify_response_code(self.app.post("/api/v1/housings"), 400)

    def test_create_housing_invalid_month(self):
        self.verify_response_code(
            self.app.post(
                "/api/v1/housings",
                json={
                    "address": {
                        "number": "123",
                        "street": "Main St",
                        "extra": "APT 456",
                        "city": "Nowhere",
                        "state": "NE",
                        "zip_code": "98765",
                        "tags": [],
                    },
                    "start_month": "16",  # Month out of range
                    "start_year": "2020",
                    "end_month": "4",
                    "end_year": "2020",
                    "monthly_payment": 1545,
                    "tags": [],
                },
            ),
            400,
        )

    def test_create_housing_invalid_year(self):
        self.verify_response_code(
            self.app.post(
                "/api/v1/housings",
                json={
                    "address": {
                        "number": "123",
                        "street": "Main St",
                        "extra": "APT 456",
                        "city": "Nowhere",
                        "state": "NE",
                        "zip_code": "98765",
                        "tags": [],
                    },
                    "start_month": "1",
                    "start_year": "foobar",  # Year not convertible to int
                    "end_year": "2020",
                    "monthly_payment": 1545,
                    "tags": [],
                },
            ),
            400,
        )

    # endregion

    # region Read
    def test_get_all_housings(self):
        response = self.verify_response_code(self.app.get("/api/v1/housings"), 200)
        housings = self.assertFieldIn(response, field="housings")
        self.assertEqual(len(housings), 2, f"Expected 2 housings in response -- {response}")

    def test_get_all_housings_paginated(self):
        response = self.verify_response_code(self.app.get("/api/v1/housings?page=2&count=1"), 200)
        housings = self.assertFieldIn(response, field="housings")
        self.assertEqual(len(housings), 1, f"Expected just 1 housing in response -- {response}")

    def test_get_single_housing(self):
        response = self.verify_response_code(
            self.app.get(f"/api/v1/housings/{self.ids_to_cleanup[0]}"), 200
        )
        start_month = self.assertFieldIn(response, field="start_month")
        self.assertEqual(start_month, "1", f"Unexpected start_month '{start_month}'")

    def test_get_single_nonexistent_housing(self):
        self.verify_response_code(self.app.get("/api/v1/housings/5f0113731c990801cc5d3240"), 404)

    # endregion

    # region Update
    def test_update_housing(self):
        response = self.verify_response_code(
            self.app.put(
                f"/api/v1/housings/{self.ids_to_cleanup[0]}",
                json={
                    "address": {
                        "number": "123",
                        "street": "Main St",
                        "extra": "APT 456",
                        "city": "Nowhere",
                        "state": "NE",
                        "zip_code": "98765",
                    },
                    "start_month": "9",
                    "start_year": "2020",
                    "end_month": "5",
                    "end_year": "2020",
                    "monthly_payment": 1545,
                    "tags": [],
                },
            ),
            200,
        )
        start_month = self.assertFieldIn(response, field="start_month")
        self.assertEqual(start_month, "9", "'start_month' field did not update correctly")
        end_month = self.assertFieldIn(response, field="end_month")
        self.assertEqual(
            end_month,
            self.test_housings[0]["end_month"],
            "'end_month' field was updated but shouldn't have been",
        )

    def test_update_housing_extra_field(self):
        self.verify_response_code(
            self.app.put(
                f"/api/v1/housings/{self.ids_to_cleanup[0]}",
                json={
                    "address": {
                        "number": "123",
                        "street": "Main St",
                        "extra": "APT 456",
                        "city": "Nowhere",
                        "state": "NE",
                        "zip_code": "98765",
                    },
                    "start_month": "9",
                    "start_year": "2020",
                    "end_month": "5",
                    "end_year": "2020",
                    "foo": "bar",  # Extra field, should throw error
                    "monthly_payment": 1545,
                    "tags": [],
                },
            ),
            400,
        )

    def test_update_housing_missing_required_field(self):
        self.verify_response_code(
            self.app.put(
                f"/api/v1/housings/{self.ids_to_cleanup[0]}",
                json={
                    "address": {
                        "number": "123",
                        "street": "Main St",
                        "extra": "APT 456",
                        "city": "Nowhere",
                        "state": "NE",
                        "zip_code": "98765",
                    },
                    "start_year": "2020",
                    "end_month": "5",
                    "end_year": "2020",
                    "monthly_payment": 1545,
                    "tags": [],
                },
            ),
            400,
        )

    def test_update_housing_missing_optional_field_is_empty(self):
        response = self.verify_response_code(
            self.app.put(
                f"/api/v1/housings/{self.ids_to_cleanup[0]}",
                json={
                    "address": {
                        "number": "123",
                        "street": "Main St",
                        "extra": "APT 456",
                        "city": "Nowhere",
                        "state": "NE",
                        "zip_code": "98765",
                    },
                    "start_month": "9",
                    "start_year": "2020",
                    "end_year": "2020",
                    "monthly_payment": 1545,
                    "tags": [],
                },
            ),
            200,
        )
        start_month = self.assertFieldIn(response, field="start_month")
        self.assertEqual(start_month, "9", "'start_month' field did not update correctly")
        end_month = self.assertFieldIn(response, field="end_month")
        self.assertEqual(
            end_month, "", f"Expected 'end_month' field to be empty but it was '{end_month}'"
        )

    # endregion

    # region Delete
    def test_delete_housing(self):
        with self.datastore(Housing, config=self.config) as db:
            new_id = db.create(
                Housing.from_request(
                    {
                        "address": {
                            "number": "123",
                            "street": "Main St",
                            "extra": "APT 456",
                            "city": "Nowhere",
                            "state": "NE",
                            "zip_code": "98765",
                        },
                        "start_month": "1",
                        "start_year": "2020",
                        "end_month": "5",
                        "end_year": "2020",
                        "monthly_payment": 1545,
                        "tags": [],
                    }
                )
            )
            self.ids_to_cleanup.append(new_id)
        response = self.verify_response_code(self.app.delete(f"/api/v1/housings/{new_id}"), 204)
        self.assertEqual(response, {}, f"Expected empty response -- {response}")

    def test_delete_nonexistent_housing(self):
        self.verify_response_code(self.app.delete("/api/v1/housings/5f0113731c990801cc5d3240"), 404)

    # endregion
