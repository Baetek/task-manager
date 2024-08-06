"""
 For real use it might have been nice to parse the json responses back into a model / schema 
 so we can access fields like task.title instead of task["title"] for better IDE integration
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from app.database import db_session, engine, Base
from app.schemas import UserCreate, TaskCreate, TaskUpdate
from app.models import User, Task, TaskHistory
from app.main import create_app
from app.config import is_running_under_pytest

@pytest.fixture(scope="module")
def client():
    """
    I am using scope module here to make the tests shorter
    A more proper way could be to scope function to get a fresh DB per test.
    That way errors could be traced back more easily
    """
    app = create_app()
    with TestClient(app) as test_client:
        Base.metadata.create_all(bind=engine)
        yield test_client
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def session():
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_create_user(client):

    response = client.post(
        "/users/",
        json={"username": "testuser", "password": "password123"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_read_tasks(client):
    response = client.get("/users/1/tasks/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_task(client):
    response = client.post(
        "/users/1/tasks/",
        json={"title": "Test Task1", "description": "This is a test task"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Test Task1"

def test_update_task(client):
    response = client.post(
        "/users/1/tasks/",
        json={"title": "Test Task2", "description": "This is a test task"}
    )
    task_id = response.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}/",
        json={"title": "Updated Test Task"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Test Task"

def test_delete_task(client, session):
    """
    To check that the deleted task is moved to the TaskHistory table,
    I can either make a new API endpoint to query TaskHistory
    or query the DB directly here. 
    I have already demonstrated making API endpoints so I choose to try to call the DB from here
    """
    response = client.get("/users/1/tasks/")
    json = response.json()
    task = json[0]

    response = client.delete(f"/tasks/{task["id"]}")
    assert response.status_code == 200

    deleted_task = session.query(TaskHistory).filter(TaskHistory.id == task["id"]).first()

    assert deleted_task.title == task["title"]
    assert deleted_task.description == task["description"]
    assert deleted_task.owner_id == task["owner_id"]
    assert str(deleted_task.status) == "TaskStatus.PENDING"

    response = client.get("/users/1/tasks/")
    json = response.json()
    new_first_task = json[0]

    assert new_first_task["title"] != task["title"]

