import pytest
from minerva import create_app


@pytest.fixture
def app():
    app = create_app({"TESTING": True})
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


def test_basic(client):
    response = client.get("/api/v1/notes")
    print(response)
