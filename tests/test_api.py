import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.database import Base, get_db
from src.main import app

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


def sample_payload(program_id="P100"):
    return {
        "program_id": program_id,
        "department": "Computing",
        "partnership_type": "Nonprofit",
        "impact_area": "Education",
        "satisfaction": 4.6,
        "funding": 12500,
        "student_volunteers": 24,
    }


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_and_filter_program():
    created = client.post("/programs", json=sample_payload())
    assert created.status_code == 201
    response = client.get("/programs", params={"department": "Computing"})
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["program_id"] == "P100"


def test_rejects_duplicate_program_id():
    assert client.post("/programs", json=sample_payload()).status_code == 201
    duplicate = client.post("/programs", json=sample_payload())
    assert duplicate.status_code == 409


def test_rejects_invalid_satisfaction():
    payload = sample_payload()
    payload["satisfaction"] = 6.0
    response = client.post("/programs", json=payload)
    assert response.status_code == 422


def test_department_analytics_uses_sql_aggregation():
    client.post("/programs", json=sample_payload("P101"))
    second = sample_payload("P102")
    second["funding"] = 7500
    second["student_volunteers"] = 16
    second["satisfaction"] = 4.2
    client.post("/programs", json=second)

    response = client.get("/analytics/departments")
    assert response.status_code == 200
    row = response.json()[0]
    assert row["department"] == "Computing"
    assert row["programs"] == 2
    assert row["total_funding"] == 20000.0
    assert row["volunteers"] == 40
    assert row["average_satisfaction"] == 4.4
