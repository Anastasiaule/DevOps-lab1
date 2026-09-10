import pytest
from app import create_app

@pytest.fixture()
def client(tmp_path):
    app = create_app()
    app.config["TESTING"] = True
    app.config["DATABASE"] = str(tmp_path / "test.db")

    with app.app_context():
        from app.database import create_tables
        create_tables()

    with app.test_client() as client:
        yield client
