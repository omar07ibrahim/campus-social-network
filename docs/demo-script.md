# Demo Script (≤ 3 minutes)

> Lead: Omar (setup + demo prep, per assignment brief).

## Before the demo
1. `cd backend && source .venv/bin/activate && uvicorn main:app --reload --port 8000`
2. `cd frontend && python3 -m http.server 5500`
3. Open http://localhost:5500 in a browser, http://localhost:8000/docs in another tab
   (optional, shows the live API contract).

## Script (target: under 3 minutes)

| Time | Action | What it shows |
|---|---|---|
| 0:00–0:20 | State the problem in one sentence (from `scope.md`) | Grounds the demo in the requirement, not just "look, code" |
| 0:20–0:40 | Show the empty feed at http://localhost:5500 | `GET /posts` on load, matches `api-contract.md` |
| 0:40–1:10 | Fill the form, submit a valid post | `POST /posts` → 201 → post appears at top — full flow: browser form → backend validation → response → display (assignment's required demo flow) |
| 1:10–1:30 | Submit an empty/invalid post | 422 validation error shown inline — contract's error case, not just the happy path |
| 1:30–1:50 | Open http://localhost:8000/docs briefly | Shows the contract is live/enforced by the backend, not just described in a doc |
| 1:50–2:30 | One sentence each on what's *not* in the POC and why (auth, DB, moderation, AI) | Sets up the Assignment 2 pitch — ties to ADR-01/02/03/04 |
| 2:30–3:00 | One sentence on Assignment 2 direction (React, WebSockets, Postgres, LLM summary) | Closes on the architecture, not just the POC |

## Fallback if live demo breaks
- `backend/test_main.py` passing (`pytest -q`) is the backup evidence the contract holds,
  screenshot it before the exam if live demo access is uncertain.
