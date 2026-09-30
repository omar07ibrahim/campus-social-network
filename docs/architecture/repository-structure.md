# Repository Structure (2.5)

> Owners: Makar (backend), Omar (frontend). This documents the actual repo layout as of the
> Assignment 1 POC, plus what Assignment 2 adds.

## Current (Assignment 1 POC)

```
campus-social-network/
├── README.md                  setup/run instructions, team, POC simplifications
├── backend/
│   ├── main.py                 FastAPI app: POST/GET /posts, GET /health
│   ├── test_main.py            pytest suite (4 tests, run: pytest -q)
│   └── requirements.txt        fastapi, uvicorn, pytest, httpx
├── frontend/
│   ├── index.html               post form + feed
│   └── app.js                   fetch calls to the backend, matches api-contract.md
└── docs/
    ├── requirements/
    │   ├── scope.md              1.1 product scope
    │   ├── stakeholders.md       1.1 stakeholder analysis + conflicts
    │   ├── functional-requirements.md    1.2
    │   ├── non-functional-requirements.md 1.3 (+ 2.1 driver ranking)
    │   ├── user-stories.md       1.4-1.5, traceability matrix
    │   └── requirements-review.md 1.5
    ├── architecture/
    │   ├── api-contract.md       2.4 interface contract (POC)
    │   ├── repository-structure.md  2.5 (this file)
    │   ├── adr/                  2.7 — adr-01..adr-04
    │   └── diagrams/             2.2-2.3, 2.6 — C4, sequence, ER (Mermaid)
    └── project-management/
        └── README.md             Section 3
```

## Assignment 2 target (planned, not yet built)

```
campus-social-network/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── models/              SQLModel/SQLAlchemy models (User, Group, Post, Comment,
│   │   │                        ModerationRecord, Draft — see er-diagram.md)
│   │   ├── routers/             posts.py, comments.py, moderation.py, ws.py
│   │   ├── services/             thread-summarization client (ADR-02)
│   │   └── db.py
│   ├── alembic/                 schema migrations (ADR-03)
│   └── tests/
├── frontend/
│   ├── src/
│   │   ├── components/           React components (feed, post form w/ rich text, moderation UI)
│   │   └── api/                  typed client for the backend contract
│   └── package.json
└── docs/                        same structure as A1, sections filled in further
```

## Rationale
- `backend/` and `frontend/` are separate top-level dirs (not a monorepo tool like Nx/Turborepo)
  — team is 4 people, 2 assignments; that tooling overhead isn't justified yet.
- `docs/` mirrors the assignment's own section numbering (1.x requirements, 2.x architecture,
  3.x project management) so any grader — or teammate — can find a section without guessing.
- Assignment 2's `backend/app/` split (models/routers/services) follows ADR-03 (relational
  data needs real model classes) and ADR-04 (concurrency logic lives in a service, not
  scattered across route handlers).
