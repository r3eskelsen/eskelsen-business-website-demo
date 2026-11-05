# ESK-LAB-11 — Independent Verification Report

**Date:** 2026-11-05  
**Source:** `eskelsen-business-website-demo.zip`  
**Source SHA-256:** `020238259ed9494f5af11d27d13378caa99207b8471cb1eaa88de24d10ccf671`  
**Original ZIP unchanged:** Yes.

## Overall result

**25/25 checks passed** in a clean extracted copy using Python 3.13.5 and Chromium 144.0.7559.96. An additional eight keyboard-first-focus checks (four pages at two viewport sizes) also passed. The project’s eight existing pytest tests passed independently (`8 passed in 0.28s`). The user separately supplied a Windows Python 3.12.10 test run (`8 passed, 1 warning`), and confirmed responsive/connectivity checks on their system. That Windows test was not independently run by this verifier.

**This is a local-only, synthetic-data portfolio demonstration, not a public deployment, independent screen-reader certification, WCAG compliance audit, or production-hardening verification.**

## Verification and acceptance matrix

| ID | Area | Observed status | Scope |
|---|---|---|---|
| T01–T09 | Existing automated tests | **PASS (8/8)** | Extracted project, real pytest, temporary database |
| M01 | Keyboard / form validation | **PASS in Chromium-rendered source** | Four pages: skip link then brand focus, at 375/1440px; contact form input focus, required labels, live status and invalid submission. Not a physical screen-reader test |
| M02 | Responsive viewports | **PASS in Chromium-rendered source** | 375/768/1440px × 4 pages: zero horizontal overflow; 12 screenshots |
| M03 | Network error | **PASS for simulated fetch failure** | Original client JS displayed an honest network error; database count unchanged; actual DevTools offline HTTP not exercised |
| Form happy path | Persist fictional lead | **PASS with controlled browser→backend bridge** | Original HTML/CSS/JS rendered in Chromium; JavaScript fetch routed through test bridge to actual FastAPI HTTP server and SQLite, one row added; form reset and local-only confirmation |
| HTTP server | Routing and assets | **PASS** | Actual loopback HTTP GET for 4 pages, CSS/JS, health; unknown path 404 and internal link targets resolve |
| Error 503 UI | Error display | **PASS, mocked frontend response** | Original JS showed no false success; backend 503 also covered separately in pytest |
| M04 | Clean setup | **PARTIAL** | Fresh extraction, successful Python tests, local server boot on Linux. Fresh offline dependency install unavailable (no FastAPI wheel cached). Existing Windows venv run passed per user log; no new-venv Windows install proven |

## Browser test implementation / limitations

Chromium in this container returns `ERR_BLOCKED_BY_ADMINISTRATOR` when attempting to navigate to `http://127.0.0.1` or `file://`. This is a platform restriction, not an observed application defect. To preserve useful independent verification, the tests loaded the original static HTML/CSS/JavaScript content into a Chromium document (script injected after parse, matching `defer` execution). No application source modification was made. A test-only fetch bridge sent payloads to the **actual locally running FastAPI server** with a temporary SQLite file. Offline and HTTP 503 conditions were exercised as **simulations** in the browser. These are not equivalent to an unrestricted browser HTTP end-to-end or hardware screen-reader audit.

The test server bound only `127.0.0.1:18765` and was stopped. All stored data was fictional. The temporary SQLite database and local server logs are **not** included in the public source archive.

## Remaining acceptance limitations

1. **Direct browser HTTP end-to-end** test under an environment that permits `127.0.0.1`, including browser DevTools offline (simulated here).
2. **Actual assistive-technology verification** (e.g. NVDA or VoiceOver) if claiming screen-reader compatibility / WCAG support. Automated semantic checks alone do not establish it.
3. **Fresh dependency install on a new Windows venv**. Existing `.venv` tests pass, but an independent offline dependency install could not be completed in this sandbox due absent cached packages.
4. Owner human publication approval and inspection for authorship/third-party rights remain separate from technical testing.

## Release status

**G3 automated PASS; independent responsive/keyboard and local backend checks PASS; M03 simulated PASS; M04 PARTIAL; G5 CONDITIONAL/HOLD for a claim of *full manual acceptance*.** The repository can be represented as a working **local synthetic demonstration**, as long as these limitations are explicit; do not describe it as production-ready or WCAG-certified.

## Evidence package

`evidence/pytest_run.txt`, `evidence/audit_results.json`, `evidence/keyboard_all_pages.json`, screenshots named `<page>_<width>px.png` and `contact_network_error_1440px.png`. The original ZIP SHA-256 above provides the exact source baseline.
