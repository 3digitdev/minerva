from minerva import MongoConnector
from minerva.categories.dates import Date
from .test_categories_base import CategoriesTestsBase


class DatesTests(CategoriesTestsBase):
    def setUp(self) -> None:
        self.item_type = Date
        super().setUp()
        self.test_dates = [
            {
                "name": "An Anniversary",
                "day": "25",
                "month": "4",
                "year": "1924",
                "subject": "Mom and Dad",
                "notes": ["don't forget", "buy them a gift"],
                "tags": [],
            },
            {
                "name": "A Birthday",
                "day": "16",
                "month": "2",
                "year": "",
                "subject": "",
                "notes": [],
                "tags": [],
            },
        ]
        with MongoConnector(Date, is_test=True) as db:
            for date in self.test_dates:
                self.ids_to_cleanup.append(db.create(Date.from_request(date)))

    def tearDown(self) -> None:
        super().tearDown()

    # region Create
    def test_create_date(self):
        response = self.verify_response_code(
            self.app.post(
                "/api/v1/dates",
                json={
                    "name": "A Bat Mitzvah",
                    "day": "25",
                    "month": "4",
                    "year": "1924",
                    "subject": "Mom and Dad",
                    "notes": ["don't forget", "buy them a gift"],
                    "tags": [],
                },
            ),
            201,
        )
        new_id = self.assertFieldIn(response, field="id")
        self.ids_to_cleanup.append(new_id)

    def text_create_date_missing_required_field(self):
        self.verify_response_code(
            self.app.post(
                "/api/v1/dates",
                json={
                    "day": "25",
                    "month": "4",
                    "year": "1924",
                    "subject": "Mom and Dad",
                    "notes": ["don't forget", "buy them a gift"],
                    "tags": [],
                },
            ),
            404,
        )

    def test_create_date_missing_optional_field_is_empty(self):
        response = self.verify_response_code(
            self.app.post(
                "/api/v1/dates",
                json={
                    "name": "A Bat Mitzvah",
                    "day": "25",
                    "month": "4",
                    "subject": "Mom and Dad",
                    "notes": ["don't forget", "buy them a gift"],
                    "tags": [],
                },
            ),
            201,
        )
        new_id = self.assertFieldIn(response, field="id")
        self.ids_to_cleanup.append(new_id)
        date = self.assertItemExists(new_id, item_type=Date)
        self.assertIsInstance(date, Date, f"Expected '{new_id}' to yield a Date!")
        assert isinstance(date, Date)  # Shouldn't have to do this...
        self.assertEqual(date.year, "", f"Expected the 'year' to be empty, but was '{date.year}'")

    def test_create_date_missing_body(self):
        self.verify_response_code(self.app.post("/api/v1/dates"), 400)

    # endregion

    # region Read
    def test_get_all_dates(self):
        response = self.verify_response_code(self.app.get("/api/v1/dates"), 200)
        dates = self.assertFieldIn(response, field="dates")
        self.assertEqual(len(dates), 2, f"Expected 2 dates in response -- {response}")

    def test_get_single_date(self):
        response = self.verify_response_code(
            self.app.get(f"/api/v1/dates/{self.ids_to_cleanup[0]}"), 200
        )
        name = self.assertFieldIn(response, field="name")
        self.assertEqual(name, "An Anniversary", f"Unexpected name '{name}")

    def test_get_single_nonexistent_date(self):
        self.verify_response_code(self.app.get("/api/v1/dates/5f0113731c990801cc5d3240"), 404)

    # endregion

    # region Update
    def test_update_date(self):
        response = self.verify_response_code(
            self.app.put(
                f"/api/v1/dates/{self.ids_to_cleanup[0]}",
                json={
                    "name": "A Quincenera",
                    "day": "25",
                    "month": "4",
                    "year": self.test_dates[0]["year"],
                    "subject": "Mom and Dad",
                    "notes": ["don't forget", "buy them a gift"],
                    "tags": [],
                },
            ),
            200,
        )
        name = self.assertFieldIn(response, field="name")
        self.assertEqual(name, "A Quincenera", "'name' field did not update correctly")
        year = self.assertFieldIn(response, field="year")
        self.assertEqual(
            year, self.test_dates[0]["year"], "'year' field was updated but shouldn't have been"
        )

    def test_update_date_extra_field(self):
        self.verify_response_code(
            self.app.put(
                f"/api/v1/dates/{self.ids_to_cleanup[0]}",
                json={
                    "name": "A Quincenera",
                    "day": "25",
                    "month": "4",
                    "year": "1924",
                    "subject": "Mom and Dad",
                    "notes": ["don't forget", "buy them a gift"],
                    "foo": "bar",  # Extra field, should throw error
                    "tags": [],
                },
            ),
            400,
        )

    def test_update_date_missing_required_field(self):
        self.verify_response_code(
            self.app.put(
                f"/api/v1/dates/{self.ids_to_cleanup[0]}",
                json={
                    "day": "25",
                    "month": "4",
                    "year": "",
                    "subject": "",
                    "notes": [],
                    "tags": [],
                },
            ),
            400,
        )

    def test_update_date_missing_optional_field_is_empty(self):
        response = self.verify_response_code(
            self.app.put(
                f"/api/v1/dates/{self.ids_to_cleanup[0]}",
                json={
                    "name": "A Bat Mitzvah",
                    "day": "25",
                    "month": "4",
                    "subject": "",
                    "notes": [],
                    "tags": [],
                },
            ),
            200,
        )
        name = self.assertFieldIn(response, field="name")
        self.assertEqual(name, "A Bat Mitzvah", "'name' field did not update correctly")
        year = self.assertFieldIn(response, field="year")
        self.assertEqual(year, "", f"Expected 'year' field to be empty but it was '{year}'")

    # endregion

    # region Delete
    def test_delete_date(self):
        with MongoConnector(Date, is_test=True) as db:
            new_id = db.create(
                Date.from_request(
                    {
                        "name": "A Bat Mitzvah",
                        "day": "25",
                        "month": "4",
                        "year": "1924",
                        "subject": "Mom and Dad",
                        "notes": ["don't forget", "buy them a gift"],
                        "tags": [],
                    }
                )
            )
            self.ids_to_cleanup.append(new_id)
        response = self.verify_response_code(self.app.delete(f"/api/v1/dates/{new_id}"), 204)
        self.assertEqual(response, {}, f"Expected empty response -- {response}")

    def test_delete_nonexistent_date(self):
        self.verify_response_code(self.app.delete("/api/v1/dates/5f0113731c990801cc5d3240"), 404)

    # endregion
