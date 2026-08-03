import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app as app_module


@pytest.fixture
def students():
    """The application's in-memory student store, emptied for each test."""
    app_module.students.clear()
    yield app_module.students
    app_module.students.clear()


@pytest.fixture
def client(students):
    app_module.app.config['TESTING'] = True
    with app_module.app.test_client() as test_client:
        yield test_client
