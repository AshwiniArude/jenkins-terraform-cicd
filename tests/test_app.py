import pytest

from app.app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_health_returns_up(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json()["status"] == "UP"


def test_home_page_renders(client):
    res = client.get("/")
    assert res.status_code == 200
    assert b"Shipment Tracker" in res.data


def test_version_endpoint(client):
    data = client.get("/api/version").get_json()
    assert "version" in data and "build" in data


def test_list_shipments(client):
    data = client.get("/api/shipments").get_json()
    assert data["count"] >= 3
    assert len(data["shipments"]) == data["count"]


def test_get_existing_shipment(client):
    res = client.get("/api/shipments/SHP-1001")
    assert res.status_code == 200
    assert res.get_json()["mode"] == "SEA"


def test_get_missing_shipment_returns_404(client):
    assert client.get("/api/shipments/SHP-9999").status_code == 404


def test_create_shipment(client):
    payload = {"origin": "Nhava Sheva", "destination": "Hamburg", "mode": "sea"}
    res = client.post("/api/shipments", json=payload)
    assert res.status_code == 201
    body = res.get_json()
    assert body["mode"] == "SEA"
    assert body["status"] == "BOOKED"


def test_create_shipment_missing_fields(client):
    res = client.post("/api/shipments", json={"origin": "Pune"})
    assert res.status_code == 400


def test_create_shipment_invalid_mode(client):
    res = client.post("/api/shipments", json={"origin": "A", "destination": "B", "mode": "RAIL"})
    assert res.status_code == 400
