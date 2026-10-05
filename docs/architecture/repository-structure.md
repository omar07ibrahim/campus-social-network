# 2.5 Code and Repository Structure

> Lead: Makar, frontend parts with Omar. One repository for code, tests, docs and diagram
> sources, so the report, the contract and the code are reviewed together.

## Now (Assignment 1)
```
campus-social-network/
├── README.md                     setup/run instructions, POC simplifications
├── Report.pdf                    the submitted report, built from docs/
├── .github/CODEOWNERS            who reviews which area (3.1)
├── .gitignore                    keeps .env, venvs, caches out of Git
├── backend/                      Makar
│   ├── main.py                   FastAPI app: POST/GET /posts, GET /health
│   ├── test_main.py              pytest suite (8 tests)
│   └── requirements.txt
├── frontend/                     Omar
│   ├── index.html                form + feed
│   └── app.js                    fetch calls matching api-contract.md Part A
└── docs/
    ├── requirements/             Salama (1.1–1.3, 2.1), Aro (1.4–1.5)
    ├── architecture/
    │   ├── api-contract.md       2.4 (Makar)
    │   ├── behaviour-and-design.md  2.3 (Omar, Makar)
    │   ├── repository-structure.md  2.5 (this file)
    │   ├── adr/                  2.7, one ADR per member
    │   └── diagrams/             2.2, 2.3, 2.6 — Mermaid sources (editable, render on GitHub)
    ├── project-management/       Section 3 (Aro)
    ├── poc.md, demo-script.md    Section 4 (Omar, Makar)
    └── build_report.py           assembles Report.pdf (Aro)
```

## Assignment 2 target
```
campus-social-network/
├── backend/
│   ├── app/
│   │   ├── main.py               app factory, routers mounted
│   │   ├── auth.py               Auth component
│   │   ├── policy.py             Access Policy (ADR-01) — one file, heavily tested
│   │   ├── routers/              posts.py, groups.py, drafts.py, moderation.py, summaries.py, ws.py
│   │   ├── services/             drafts.py, moderation.py, summary.py, llm_adapter.py
│   │   ├── models/               SQLModel tables matching er-diagram.md
│   │   ├── repositories/         queries and transactions
│   │   └── settings.py           reads configuration from environment variables
│   ├── alembic/                  database migrations (ADR-03)
│   ├── tests/
│   │   ├── unit/                 policy, services (LLM and DB mocked)
│   │   ├── api/                  endpoint tests incl. role × endpoint authorization matrix
│   │   └── contract/             responses validated against openapi.json
│   ├── .env.example              variable names only, no values
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   │   ├── components/           Feed, PostEditor (rich text), DraftEditor, ModerationQueue, SummaryPanel
│   │   ├── api/                  typed client generated from openapi.json
│   │   ├── realtime/             WebSocket client, reconnect + refetch
│   │   └── pages/
│   ├── tests/                    component tests (Vitest) + Playwright end-to-end
│   ├── .env.example              only public values (API base URL)
│   └── package.json
├── shared/
│   └── openapi.json              exported from FastAPI; the single shared contract
├── docker-compose.yml            api + postgres + mock identity provider for local dev
├── .github/workflows/ci.yml      tests, lint, secret scan on every pull request
└── docs/                         same layout as now
```

## How the structure reflects the architecture and the team
- Top-level folders match the C4 containers: `frontend/` = Web App, `backend/` = Backend API
  (+ Realtime hub), the database is defined by `backend/app/models` and `alembic/`.
- Inside `backend/app/`, files match the components in `diagrams/c4-component.md`, so a
  reviewer can go from diagram box to file directly.
- The only shared code is the contract: FastAPI exports `openapi.json`, the frontend's API
  client is generated from it. A contract change shows up as a diff in one file that both
  Makar and Omar review.
- `docs/` follows the report's numbering. `.github/CODEOWNERS` maps each folder to its lead,
  so GitHub requests the right reviewer automatically (Section 3.1).

## Keeping secrets out of the repository and browser code
- Secrets (database password, LLM API key, OIDC client secret, session signing key) are read
  from environment variables in `settings.py`. Locally they live in `backend/.env`, which is
  in `.gitignore`; only `.env.example` with variable names is committed.
- The browser never receives a secret: LLM and identity-provider calls are made by the
  backend. The frontend `.env` holds only public values (e.g. API base URL), because anything
  bundled into JavaScript is readable by users.
- The session is an `HttpOnly` cookie, so page scripts cannot read it.
- CI runs a secret scanner (gitleaks) on every pull request; a leaked key is rotated, not just
  deleted from history.
- The Assignment 1 POC needs no secrets at all.
