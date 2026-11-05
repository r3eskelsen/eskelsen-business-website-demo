"""Isolated synthetic-lead capture lab; NOT a production CRM."""
import os
import re
import sqlite3
import threading
import time
from collections import defaultdict, deque
from pathlib import Path
from contextlib import asynccontextmanager
from typing import Literal

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

ROOT = Path(__file__).resolve().parent
APP_ROOT = ROOT.parent
STATIC = ROOT / "static"
DB_PATH = Path(os.getenv("ESK_DB_PATH", str(APP_ROOT / "local_leads.sqlite3")))
RATE_LIMIT = max(1, int(os.getenv("ESK_RATE_LIMIT", "5")))
RATE_WINDOW = max(1, int(os.getenv("ESK_RATE_WINDOW", "60")))
_rate_lock = threading.Lock()
_requests = defaultdict(deque)
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="Eskelsen Systems Business Website Lab", docs_url=None, redoc_url=None, lifespan=lifespan)
app.mount("/static", StaticFiles(directory=STATIC), name="static")

class Lead(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str = Field(min_length=2, max_length=80)
    email: str = Field(min_length=5, max_length=254)
    service: Literal["Business website", "API integration", "Technical consultation"]
    message: str = Field(min_length=10, max_length=1500)
    website: str = Field(default="", max_length=250)  # honeypot
    consent: bool

    @field_validator("name", "message")
    @classmethod
    def validate_text(cls, v: str):
        v = v.strip()
        if not v or any(ord(ch) < 32 and ch not in "\n\t" for ch in v):
            raise ValueError("Invalid text")
        return v

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str):
        v = v.strip().lower()
        # Basic format validation only; not proof of address ownership.
        if not re.fullmatch(r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+", v):
            raise ValueError("Enter a valid email address")
        return v


def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at INTEGER NOT NULL,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            service TEXT NOT NULL,
            message TEXT NOT NULL
        )""")

@app.middleware("http")
async def headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; base-uri 'none'; frame-ancestors 'none'; form-action 'self'"
    response.headers["Cache-Control"] = "no-store" if request.url.path.startswith("/api") else "public, max-age=300"
    return response

@app.get("/", include_in_schema=False)
def home():
    return FileResponse(STATIC / "index.html")

@app.get("/{page}", include_in_schema=False)
def page(page: str):
    if page not in {"services", "about", "contact"}:
        raise HTTPException(status_code=404, detail="Not found")
    return FileResponse(STATIC / f"{page}.html")

@app.get("/api/health")
def health():
    return {"status": "ok", "mode": "local-demo"}

@app.post("/api/leads", status_code=201)
def submit(lead: Lead, request: Request):
    if lead.website:
        # No persistence for likely bots; identical response to reduce oracle signal.
        return JSONResponse(status_code=201, content={"status": "received", "demo": True})
    if lead.consent is not True:
        raise HTTPException(status_code=422, detail="Consent is required")
    # Demo-only in-memory per-IP limiter; trusted proxy not supported.
    ip = request.client.host if request.client else "unknown"
    now = time.monotonic()
    with _rate_lock:
        q = _requests[ip]
        while q and now - q[0] >= RATE_WINDOW:
            q.popleft()
        if len(q) >= RATE_LIMIT:
            raise HTTPException(status_code=429, detail="Too many requests. Try again later.")
        q.append(now)
    try:
        with sqlite3.connect(DB_PATH, timeout=3) as conn:
            conn.execute(
                "INSERT INTO leads (created_at,name,email,service,message) VALUES (?,?,?,?,?)",
                (int(time.time()), lead.name, lead.email, lead.service, lead.message),
            )
    except sqlite3.Error:
        raise HTTPException(status_code=503, detail="Local demo storage is temporarily unavailable")
    return {"status": "received", "demo": True}
