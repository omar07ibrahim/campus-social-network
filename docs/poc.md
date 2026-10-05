# 4 Proof of Concept

> Leads: Makar (backend), Omar (frontend, README, demo). Validated against US-1/US-2
> acceptance criteria by Aro and against FR-1/FR-2 by Salama.

## What it demonstrates
One complete interaction from the planned architecture — **creating a campus post**:
browser form → `POST /posts` → backend validation → 201 response → post shown at the top of
the feed. On load the page calls `GET /posts` to show existing posts newest first. Invalid
input returns 422 and the page shows a readable error.

| Part | File | Owner |
|---|---|---|
| Backend (FastAPI) | `backend/main.py` | Makar |
| Backend tests (8) | `backend/test_main.py` | Makar |
| Frontend (HTML + JS) | `frontend/index.html`, `frontend/app.js` | Omar |
| Contract | `docs/architecture/api-contract.md` Part A | Makar & Omar |
| Run instructions | `README.md` | Omar |
| Demo plan | `docs/demo-script.md` | Omar |

## Request and response match the contract
- Request `{author, content}` and the 201 body `{id, author, content, created_at}` are the
  Pydantic models in `main.py`; FastAPI serves the same schema at `/docs`.
- The 422 body is FastAPI's standard shape, as documented; `app.js` reads `detail[].loc`
  and `detail[].msg` from exactly that shape.
- Tests assert status codes, fields, ordering and error shapes.

## Acceptance check (Aro, Salama)
| Criterion | Result |
|---|---|
| US-1: valid post appears at the top of the feed without reload | Pass (browser test) |
| US-1: empty content → validation error, nothing created | Pass (`test_create_post_missing_content_returns_422`, `test_whitespace_only_content_returns_422`, browser) |
| US-2: posts newest first | Pass (`test_list_posts_newest_first`) |
| US-2: empty feed shows no error | Pass (`test_list_posts_empty`, browser) |
| FR-1 length rule 1–1000 | Pass (`test_content_over_1000_chars_returns_422`) |

## What we simplified from the planned architecture
| Planned (Assignment 2) | In the POC | Why it is acceptable here |
|---|---|---|
| React + rich-text editor | Plain HTML + JavaScript | Brief says React is not needed; same request/response either way |
| University sign-in, roles | `author` is free text | Shows the flow without an identity provider |
| PostgreSQL (ADR-03) | In-memory Python list, cleared on restart | No setup for the demo; storage is behind the endpoint, so it can be swapped |
| Access Policy, groups, visibility | Every post is public | Single interaction only |
| WebSocket live updates | Page shows its own new post; others appear on reload | Brief says live updates are not needed |
| LLM summaries | Not present | Brief says AI integration is not needed |
| CORS restricted to the web app origin | CORS `*` | Local demo on two ports |
| Uniform error envelope for non-422 errors | Only 422 can occur | No auth/conflict cases exist yet |
