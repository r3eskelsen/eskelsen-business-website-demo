# LAB-11 — G3 / G4 / G5 Verification Record

**Recorded:** 2026-11-05. **Release category:** public local synthetic demonstration.

| Gate/check | Status | Evidence and limitation |
|---|---|---|
| G0 scope | DOCUMENTED | `docs/SCOPE_G0.md` |
| G1 environment | PARTIAL | Windows Python 3.12.10, 8/8 pytest reported by owner; independent Linux Python 3.13.5, 8/8; new offline venv dependency download not proven |
| G2 implementation | COMPLETE (demo scope) | Four standalone HTML/CSS/JS pages, FastAPI and local SQLite |
| G3 automated | PASS | 8/8 pytest in independent extraction and owner's Windows run; one Starlette/TestClient deprecation warning was reported by owner |
| G3 HTTP API | PASS in local service | Prior recorded checks and fresh 13/13 loopback smoke: GET four pages/assets/health, invalid route, validation, honeypot and synthetic lead persisted to temporary DB |
| M01 keyboard | PASS in controlled Chromium source rendering | Logical first-focus/skip-link tests on four pages at 375/1440px; not an NVDA/VoiceOver test |
| M02 responsive | PASS in controlled Chromium source rendering | Four pages, 375px/768px/1440px screenshots, no horizontal overflow; owner separately confirmed sizes |
| M03 network failure | PASS **in simulation** | Original client JS showed truthful error on mocked network failure, no write; not actual browser DevTools offline over HTTP |
| Form happy path | PASS in controlled Chromium bridge | Unchanged JS executed; test bridge delivered request to real local FastAPI HTTP endpoint and temporary SQLite; not full direct browser HTTP |
| M04 clean setup | PARTIAL | Fresh extraction / app boot / tests on Linux; fresh dependency installation in new offline venv not possible; existing Windows venv passed |
| G4 public package | READY | MIT, source, evidence, release limitations, manifest and publication instructions |
| G5 complete manual certification | CONDITIONAL | Direct unrestricted browser HTTP test and real screen-reader assessment are not demonstrated; not required to represent a limited local demo honestly |
| G6 production | NOT PERFORMED | This demo is not a real live client website or certified production system |

## Publication decision

**APPROVED FOR PUBLICATION AS A LAB DEMONSTRATION ONLY**, provided the owner confirms authorship/distribution rights and publishes from this verified package. There is no claim that complete G5 manual certification, WCAG compliance, production hardening, or commercial use has been achieved.

For procedural detail see `evidence/INDEPENDENT_AUDIT_REPORT_20261105.md` and fresh `evidence/RELEASE_LOOPBACK_HTTP_SMOKE_20261105.txt`. Tests use fictional submissions. The original submitted ZIP and the owner's Windows workspace were not modified by this packaging work.
