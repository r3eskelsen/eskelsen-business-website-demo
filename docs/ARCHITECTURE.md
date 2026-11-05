# Architecture — ESK-LAB-11

```text
Local browser (127.0.0.1)
  ├── GET /, /services, /about, /contact → static responsive pages
  ├── GET /static/* → first-party CSS / JavaScript
  └── POST /api/leads → Pydantic allow-list validation
                           ├── honeypot filter
                           ├── single-process in-memory rate limit
                           └── parameterized INSERT → local SQLite
```

**Trust boundary:** local loopback only. No authentication, no real personal data, no public hosting. Reverse proxies, WAF/CDN, background jobs, email and multi-worker state are intentionally absent. API rejects unexpected fields, applies minimal headers, and does not expose submitted leads through a GET endpoint. There is no deletion scheduler; data removal is by destroying the disposable local database while stopped.

**Files:** `src/app.py` is the FastAPI entry point; `src/static/` owns all four standalone pages, styling and client-side logic; `tests/` uses a temporary SQLite database; `evidence/` contains sanitized test evidence. SQLite is created at start and ignored by Git. The rate limiter uses process memory, so restarting clears its counts.

**Scope:** independently implemented synthetic lead capture for portfolio demonstration. No claims of production readiness.
