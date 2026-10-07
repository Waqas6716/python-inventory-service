from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    assert client.get("/health").json() == {"status": "ok"}


def test_reservation_is_idempotent():
    headers = {"Idempotency-Key": "reservation-0001"}
    first = client.post("/v1/reservations", json={"sku": "SKU-DESK-01", "quantity": 1}, headers=headers)
    second = client.post("/v1/reservations", json={"sku": "SKU-DESK-01", "quantity": 1}, headers=headers)
    assert first.status_code == 201
    assert second.json() == first.json()
