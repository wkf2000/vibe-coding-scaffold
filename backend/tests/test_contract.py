from fastapi.testclient import TestClient
from app.main import app


def test_healthz() -> None:
    c = TestClient(app)
    r = c.get("/healthz")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_enrich_rejects_empty_text() -> None:
    c = TestClient(app)
    r = c.post("/v1/enrich", json={"text": ""})
    assert r.status_code in (400, 422)
