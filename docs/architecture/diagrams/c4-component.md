# 2.2 C4 — Level 3: Components of the Backend API

> Lead: Makar (backend component diagram, as assigned in the brief). Selected container:
> **Backend API** — it holds every rule the requirements care about (authorization,
> validation, moderation, concurrency, AI checks), so it is the container most worth
> decomposing.

```mermaid
flowchart LR
    spa["<b>Web App</b><br/>[Container: React]<br/>Feed, editor, drafts, moderation UI"]
    idp["<b>University sign-in</b><br/>[External system: OIDC]"]
    llm["<b>LLM Provider</b><br/>[External system]"]
    db[("<b>Database</b><br/>[Container: PostgreSQL]")]

    subgraph api["Backend API — FastAPI container"]
        direction LR
        auth["<b>Auth</b><br/>[FastAPI dependency]<br/>Session cookie, current user"]
        subgraph routers[" "]
            direction TB
            posts["<b>Posts & Comments router</b><br/>Create/list, Pydantic validation"]
            groups["<b>Groups router</b><br/>Membership, officers, verification"]
            drafts["<b>Drafts service</b><br/>Versioned saves, publish (ADR-04)"]
            moderation["<b>Moderation service</b><br/>Reports, hide, appeals, audit"]
            summary["<b>Summary service</b><br/>Visible comments, citation check (ADR-02)"]
        end
        hub["<b>Realtime hub</b><br/>[WebSocket]<br/>Subscriptions, presence, per-recipient filtering"]
        policy["<b>Access Policy</b><br/>[Python module]<br/>All visibility and role checks (ADR-01)"]
        repo["<b>Repositories</b><br/>[SQLModel]<br/>Queries, transactions (ADR-03)"]
    end

    spa -- "HTTPS/JSON (REST)" --> routers
    spa -- "WebSocket" --> hub
    spa -- "Sign-in redirect" --> auth
    auth -- "OIDC" --> idp
    routers -- "may this user see/do this?" --> policy
    hub -- "filter each event per recipient" --> policy
    routers -- "publish events after writes" --> hub
    routers -- "read/write" --> repo
    summary -- "summarize(comments) HTTPS" --> llm
    repo -- "SQL (asyncpg)" --> db
```

## Responsibilities
| Component | Responsible for | Not responsible for |
|---|---|---|
| Auth | Turning the identity provider's answer into a session; rejecting non-university emails (FR-11) | Deciding what a user may see |
| Access Policy | Every "may this user see/do this?" decision (FR-4, FR-6, FR-14, NFR-10) | Storing data |
| Posts & Comments router | Request validation (Pydantic), creating/listing posts and comments | Visibility rules (asks Access Policy) |
| Groups router | Membership, officer appointment, verification (FR-9, FR-12) | — |
| Drafts service | Version check on save, conflict response with latest draft, publish (FR-7, NFR-8) | Live presence (Realtime hub) |
| Moderation service | Reports, hide/remove, appeals, writing moderation and audit rows in one transaction (NFR-5, NFR-12) | — |
| Summary service | Selecting visible comments, calling the LLM adapter, dropping uncited points (FR-8, FR-15) | Choosing the model vendor (adapter config) |
| Realtime hub | WebSocket connections, subscriptions, presence, delivering events (FR-13, NFR-4) | Accepting writes — all writes go through REST |
| Repositories | SQL queries, transactions, optimistic-lock `UPDATE` | Business rules |

The proof of concept (`backend/main.py`) contains a minimal version of the Posts router
only: Pydantic validation and an in-memory list in place of Repositories.

The five boxes in the inner frame are drawn together because they share the same three
dependencies (Access Policy, Realtime hub, Repositories); the table above lists each one's
responsibility separately.
