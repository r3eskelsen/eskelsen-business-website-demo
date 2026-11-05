# Eskelsen Systems — Business Website + Lead Capture Lab

An **independent, local-only demonstration** of a responsive business website and a validated lead intake API. It is **not** a live commercial site, deployment, production-grade security implementation, or documented customer outcome.

## Features

- Home, Services, About, Contact pages; original CSS illustration (no third-party images).
- Responsive HTML/CSS with keyboard focus indicators and skip navigation.
- Synthetic-only lead form, client-side status and errors, server-side validation.
- Honeypot, basic in-memory per-client rate limiting, SQLite insert with parameters.
- API security headers and isolated tests for positive and negative scenarios.
- No emails, CRM integration, analytics, tracking, external CDN, or external services.

## Requirements

Python 3.11+; no Docker needed. SQLite is built into Python.

### Windows PowerShell

```powershell
cd .\eskelsen-business-website-demo
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m uvicorn src.app:app --host 127.0.0.1 --port 8765
```

Open `http://127.0.0.1:8765`. The app writes `local_leads.sqlite3` within the project folder. **Use synthetic demo data only**, such as `alex@example.test`. Stop with Ctrl+C. To reset the lab database, stop the server then delete only `local_leads.sqlite3` in this project (no global cleanup).

### macOS / Linux

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -m pytest -q
.venv/bin/python -m uvicorn src.app:app --host 127.0.0.1 --port 8765
```

If port `8765` is occupied, choose a free **local** port; never bind `0.0.0.0` for this lab. The app intentionally has no admin interface or lead export feature.

## API contract

`POST /api/leads` JSON: `name` (2–80), `email` (basic format), `service` (one of three allowed values), `message` (10–1500), `website` (empty hidden honeypot), `consent` (`true`). On success: HTTP 201 `{"status":"received","demo":true}`; invalid: 422; limited: 429; storage unavailable: 503. `GET /api/health` is a local demo indicator.

This API makes no claim about a deliverable message to a business owner. Synthetic form submissions are saved in local SQLite only.

## Testing and evidence

`python -m pytest -q` runs route, security header, validation, persistence, spam, throttle, and storage failure tests. A separate local HTTP/SQLite release smoke test passed 13/13 checks (`evidence/RELEASE_LOOPBACK_HTTP_SMOKE_20261105.txt`). All test fixture data uses reserved example domains. See `docs/TEST_PLAN.md` and `docs/RESULTS.md`; real test output is stored under `evidence/`, within this repository.

Independent Chromium source-render checks covered four pages at 375px, 768px, and 1440px, keyboard-first-focus behavior and a simulated network failure. The lead form was also exercised against a real loopback FastAPI HTTP server through a controlled browser bridge. The owner separately reported successful local Windows responsive and connectivity checks and an 8/8 automated test run. The evidence and the limitations of that method are described in `docs/RESULTS.md` and `evidence/INDEPENDENT_AUDIT_REPORT_20261105.md`. This is **not** an unrestricted browser HTTP end-to-end test or an assistive-technology/WCAG certification.

## Architecture and limitations

See `docs/ARCHITECTURE.md`, `docs/LIMITATIONS.md`, and `docs/SCOPE_G0.md`. No production deployment is included. This is a technical learning and portfolio artifact, not an audited security product.

## Public release / GitHub

The complete public demonstration includes source code, a license, testing artifacts and reproducible instructions. It intentionally excludes local SQLite data, virtual environments, personal information and private infrastructure. `PUBLIC_SHA256_MANIFEST.txt` records the SHA-256 hash of every included file (except the manifest itself). To publish from a clean extracted folder on Windows, follow [`docs/GITHUB_PUBLICATION.md`](docs/GITHUB_PUBLICATION.md) and use `scripts/PUBLISH_TO_GITHUB.ps1`. **Bundling this ZIP does not publish or create a remote GitHub repository.**

**Release decision:** READY TO PUBLISH AS A LOCAL SYNTHETIC DEMONSTRATION, not production software. Some independent/manual acceptance remains qualified; see [`docs/RESULTS.md`](docs/RESULTS.md) and [`docs/RELEASE_STATUS.md`](docs/RELEASE_STATUS.md).

## License

MIT © 2026 Eskelsen Systems. See `LICENSE`.
