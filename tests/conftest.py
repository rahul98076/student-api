import pytest
from app import create_app
from app.extensions import db


@pytest.fixture
def client():
    app = create_app()

    app.config['TESTING'] = True

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.test_client() as client:

        with app.app_context():
            db.create_all()

        yield client

        with app.app_context():
            db.session.remove()
            db.drop_all()
