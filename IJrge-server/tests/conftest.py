# tests/conftest.py

import pytest

@pytest.fixture
def client():
    from app import app
    with app.test_client() as client:
        yield client