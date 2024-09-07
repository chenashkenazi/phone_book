import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db, Base
from app import schemas
import random


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def generate_phone_number():
    phone_number = ""
    for i in range(9):
        phone_number += str(random.randint(0, 9))
    return phone_number


def test_create_contact():
    contact_data = {
        "first_name": "Jack",
        "last_name": "Sparrow",
        "phone_number": generate_phone_number(),
        "address": "Black Pearl"
    }
    response = client.post("/contacts/", json=contact_data)
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == contact_data["first_name"]
    assert data["last_name"] == contact_data["last_name"]
    assert data["phone_number"] == contact_data["phone_number"]
    assert data["is_favorite"] is False
    assert "id" in data


def test_create_contact_fail():
    contact_data = {
        "first_name": "Jack",
        "last_name": "Sparrow",
        "phone_number": "123456789",
        "address": "Black Pearl"
    }
    client.post("/contacts/", json=contact_data)
    response = client.post("/contacts/", json=contact_data)
    assert response.status_code == 400


def test_get_contacts():
    response = client.get("/contacts/?page=1&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data) <= 10


def test_search_contact():
    contact_data = {
        "first_name": "Peter",
        "last_name": "Parker",
        "phone_number": generate_phone_number(),
        "address": "New York"
    }
    response = client.post("/contacts/", json=contact_data)
    search_text = "Peter"
    response = client.get(f"/contacts/search/?search_text={search_text}")
    assert response.status_code == 200
    data = response.json()
    assert any(contact["first_name"] == "Peter" for contact in data)


def test_update_contact():
    contact_data = {
        "first_name": "Harry",
        "last_name": "Potter",
        "phone_number": generate_phone_number(),
        "address": "Hogwarts"
    }
    response = client.post("/contacts/", json=contact_data)
    contact_id = response.json()["id"]

    update_data = {
        "first_name": "Ron",
        "last_name": "Weasley"
    }
    response = client.put(f"/contacts/{contact_id}", json=update_data)
    assert response.status_code == 200
    updated_contact = response.json()
    assert updated_contact["first_name"] == "Ron"
    assert updated_contact["last_name"] == "Weasley"


def test_delete_contact():
    contact_data = {
        "first_name": "Delete",
        "last_name": "Me",
        "phone_number": "492726581",
        "address": "Trash"
    }
    response = client.post("/contacts/", json=contact_data)
    contact_id = response.json()["id"]

    response = client.delete(f"/contacts/{contact_id}")
    assert response.status_code == 204

    response = client.get(f"/contacts/")
    data = response.json()
    assert any(contact["first_name"] != "Delete" and contact["last_name"] != "Me" for contact in data["contacts"])
