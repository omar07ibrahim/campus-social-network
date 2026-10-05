# Demo Script (≤ 3 minutes)

> Lead: Omar. Rehearse with a timer; any member should be able to run it.

## Before the demo (not timed)
1. Terminal 1: `cd backend && source .venv/bin/activate && uvicorn main:app --port 8000`
2. Terminal 2: `cd frontend && python3 -m http.server 5500`
3. Browser tab 1: http://localhost:5500 — tab 2: http://localhost:8000/docs
4. Restart the backend just before starting so the feed is empty.

## Script

| Time | Who speaks | Action | What it shows |
|---|---|---|---|
| 0:00–0:20 | Salama | One sentence on the problem and product (`scope.md`) | Why the product exists |
| 0:20–0:35 | Omar | Show the empty feed | `GET /posts` → `[]`, US-2 "empty feed, no error" |
| 0:35–1:05 | Omar | Post as "Salama": "Study group for AI1220 at 6pm" | `POST /posts` → 201 → shown at the top: form → backend validation → response → display |
| 1:05–1:20 | Omar | Post a second one, show newest-first order | US-2 ordering |
| 1:20–1:45 | Makar | Submit spaces only as content | 422 → "content: String should have at least 1 character"; nothing stored |
| 1:45–2:10 | Makar | Tab 2: `/docs`, open `POST /posts` schema | Running contract = `api-contract.md` Part A |
| 2:10–2:40 | Aro | What is simplified and why (`docs/poc.md` table) | Explains POC vs. architecture |
| 2:40–3:00 | Aro | One sentence on Assignment 2: React, WebSockets, Postgres, cited AI summaries | Links to ADRs |

## If the live demo fails
- Run `cd backend && pytest -q` (8 passed) as evidence the contract holds.
- Keep screenshots of the working flow on the laptop as a last resort.
