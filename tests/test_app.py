import os
import sqlite3
import tempfile
from pathlib import Path

# Run against an isolated temporary database; never use the normal lab database.
_tmp = tempfile.TemporaryDirectory(prefix="esk_lab11_test_")
os.environ["ESK_DB_PATH"] = str(Path(_tmp.name) / "test.sqlite3")
os.environ["ESK_RATE_LIMIT"] = "3"

from fastapi.testclient import TestClient
from src import app as app_module

VALID = {"name":"Alex Example","email":"alex@example.test","service":"Business website","message":"A fictional example project with clear goals.","website":"","consent":True}

def client():
    return TestClient(app_module.app)

def test_pages_and_unknown_route():
    with client() as c:
        for route in ["/", "/services", "/about", "/contact"]:
            response = c.get(route)
            assert response.status_code == 200
            assert "text/html" in response.headers["content-type"]
        assert c.get("/missing").status_code == 404
        assert c.get("/api/health").json()["mode"] == "local-demo"

def test_security_headers():
    with client() as c:
        r = c.get("/")
        assert r.headers["x-frame-options"] == "DENY"
        assert "default-src 'self'" in r.headers["content-security-policy"]

def test_success_and_db_insert():
    app_module._requests.clear()
    with client() as c:
        before = count()
        r = c.post("/api/leads",json=VALID)
        assert r.status_code == 201, r.text
        assert r.json()["status"] == "received"
        assert count() == before + 1

def count():
    with sqlite3.connect(app_module.DB_PATH) as db:
        return db.execute("select count(*) from leads").fetchone()[0]

def test_invalid_and_missing_consent_do_not_persist():
    app_module._requests.clear()
    with client() as c:
        before = count()
        for change in ({"email":"bad"},{"name":"x"},{"message":"short"},{"consent":False},{"service":"other"}):
            assert c.post("/api/leads",json={**VALID,**change}).status_code == 422
        assert count() == before

def test_honeypot_drops_record():
    app_module._requests.clear()
    with client() as c:
        before = count()
        r = c.post("/api/leads",json={**VALID,"website":"https://spam.example"})
        assert r.status_code == 201
        assert count() == before

def test_rate_limit():
    app_module._requests.clear()
    with client() as c:
        for _ in range(3):
            assert c.post("/api/leads",json=VALID).status_code == 201
        assert c.post("/api/leads",json=VALID).status_code == 429

def test_extra_fields_rejected():
    app_module._requests.clear()
    with client() as c:
        assert c.post("/api/leads",json={**VALID,"is_admin":True}).status_code == 422

def test_storage_error_returns_503(monkeypatch):
    app_module._requests.clear()
    # Force an inaccessible directory as DB path; startup init would fail, so change after startup.
    with client() as c:
        monkeypatch.setattr(app_module,"DB_PATH",Path(_tmp.name) / "nonexistent" / "fail.sqlite3")
        assert c.post("/api/leads",json=VALID).status_code == 503
