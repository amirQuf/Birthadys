from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import pytest
from ..database import Base
from ..main import app, get_db
from datetime import date

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_add_friend():
    json = {"name": "test_user", "birthday": "", "email": "deadpool@example.com"}
    response = client.post("/friend/add", json=json)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "deadpool@example.com"
    assert data["name"] == json["name"]
from ..models import Friend
from datetime
def setup():
    Base.metadata.create_all(bind=engine)
    

def teardown():
    Base.metadata.drop_all(bind=engine)


def test_get_friend():
    pass


def test_retrieve_all_Friends():
    response = client.post("/friend/")
    assert response.status_code == 200, response.text



@pytest.fixture
def add_some_friend(db:override_get_db):
    today = date.today()
    john_doe = Friend(name = "john Doe", Birthday = today )
    db.add(john_doe)
    db.commit()
    db.refresh(john_doe)
    return john_doe

def test_retrieve_birthday_buddies(add_some_friend):
    response = client.post("/today-birthdays")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["result"][0] == "john Doe"
