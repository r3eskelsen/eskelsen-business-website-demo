# G0 — Architecture and Scope Decision

**Status:** Scoped and implemented as an independent demonstration; runtime verification is recorded separately.

## Fictional audience and messaging

Audience: fictional small-business owner seeking a clearer website and structured inquiry flow. Messaging: calm, credible engineering, no inflated ROI claims. The hero emphasizes practical engineering; Services lists limited capabilities; About describes principles; Contact collects synthetic examples only.

## Wireframes

- **Home:** desktop masthead / left hero + original CSS technical illustration / three capability cards / CTA / footer. Mobile: stacked.
- **Services:** masthead / introduction / three service panels / CTA.
- **About:** masthead / mission statement / three principles / CTA.
- **Contact:** masthead / synthetic-data warning / two-column privacy note + form; stacked on mobile.

## Form specification

Fields: name (2–80), email (5–254, syntactic validation only), service (allow-list), message (10–1500), honeypot `website` empty, consent true. All fields except honeypot are required. JSON API validates server-side. No auto-email, no CRM, no data export; SQLite local file only. Responses: 201/422/429/503. Form communicates network errors without claiming success.

## Costs

Local development only: planned direct hosting/API/GPU expense **$0**. Python, SQLite, HTML, CSS and JS are used without paid services. Labor estimate: **12–20 engineering hours** for full implementation + manual QA and documentation, not a promised delivery window.

## Risks

| ID | Risk | Mitigation | Residual limitation |
|---|---|---|---|
| R1 | Accidental personal data in demo | Explicit notice, test data, ignore local DB | Users must respect synthetic-only rule |
| R2 | Automated spam | Honeypot and rate limit | In-memory limiter is not robust across workers |
| R3 | Local database unavailability | 503 response, isolation | No high availability |
| R4 | Form errors / poor accessibility | Server validation, focus styles, manual checklist | Manual accessibility audit pending |
| R5 | Portfolio misrepresentation | Demo labeling, evidence record | Not a real client deployment |
| R6 | Sensitive artifact publication | Ignore DB and .env; review ZIP contents | Human review required before GitHub upload |
| R7 | Untrusted deployment configuration | Loopback only, no real data | No security certification |

## Acceptance gates

G0 scope and architecture documented. G1 local environment preflight required; remote Windows environment not inspected. G2 implement local-only. G3 automated tests and manual acceptance separately reported. G4 documentation and package. G5 conditional portfolio decision. G6 out of scope until actual outreach feedback exists.
