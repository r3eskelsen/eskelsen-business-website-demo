# G3 — Test Plan

| ID | Requirement | Procedure | Expected | Evidence |
|---|---|---|---|---|
| T01 | Page routes | GET 4 pages | 200 HTML | pytest output |
| T02 | Unknown route | GET unknown | 404 | pytest output |
| T03 | Security headers | Check root headers | Defined headers | pytest output |
| T04 | Valid form and persistence | POST synthetic lead; query test DB | 201 and one row | pytest output |
| T05 | Invalid fields and consent | POST invalid variants | 422, no new rows | pytest output |
| T06 | Honeypot | POST with website filled | 201, no insert | pytest output |
| T07 | Rate limiting | POST 4 times with limit 3 | 429 on fourth | pytest output |
| T08 | Unknown fields | POST extra key | 422 | pytest output |
| T09 | Database failure | Point to nonexistent parent | 503 | pytest output |
| M01 | Keyboard navigation | Tab through 4 pages and form; submit invalid input | Logical order, visible focus, accessible errors | Manual checklist, browser screenshots |
| M02 | Responsive | Browser viewport at 375, 768, 1440px | No horizontal clipping or overlap | Manual screenshots |
| M03 | Network error | Browser devtools offline; submit | Honest error message, no success claim | Manual checklist |
| M04 | Local clean setup | Execute PowerShell setup from new clone | Starts, passes tests, no secrets | Human Windows verification |

**Method:** use isolated temporary test DB, never customer data or production services. Preserve real test output, environment versions and checksums in `evidence/`. Mark manual rows HOLD unless verified by a human browser run. Never convert inferred success into PASS.
