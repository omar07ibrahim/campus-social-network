# 2.2 C4 — Level 3: Components of the Backend API

> Lead: Makar (backend component diagram, as assigned in the brief). Selected container:
> **Backend API** — it holds every rule the requirements care about (authorization,
> validation, moderation, concurrency, AI checks), so it is the container most worth
> decomposing.

```mermaid
C4Component
    title Backend API (FastAPI) — Components

    Container(spa, "Web App", "React", "Feed, editor, drafts, moderation UI")
    ContainerDb(db, "Database", "PostgreSQL", "All persistent data")
    System_Ext(idp, "University sign-in", "OIDC (mock in dev)")
    System_Ext(llm, "LLM Provider", "Text summarisation")

    Container_Boundary(api, "Backend API") {
        Component(auth, "Auth", "FastAPI dependency", "Sign-in callback, session cookie, current user")
        Component(policy, "Access Policy", "Python module", "Single place for visibility and role checks (ADR-01)")
        Component(posts, "Posts & Comments router", "FastAPI router", "Create/list posts and comments, validation")
        Component(groups, "Groups router", "FastAPI router", "Membership, officers, verification")
        Component(drafts, "Drafts service", "FastAPI router + service", "Versioned saves, publish (ADR-04)")
        Component(moderation, "Moderation service", "FastAPI router + service", "Reports, hide/remove, appeals, audit events")
        Component(summary, "Summary service", "Service + adapter", "Builds prompt from visible comments, checks citations (ADR-02)")
        Component(hub, "Realtime hub", "FastAPI WebSocket", "Subscriptions, presence, per-recipient event filtering")
        Component(repo, "Repositories", "SQLModel", "Queries and transactions (ADR-03)")
    }

    Rel(spa, auth, "Signs in", "HTTPS redirect")
    Rel(spa, posts, "Calls", "HTTPS/JSON")
    Rel(spa, drafts, "Saves drafts", "HTTPS/JSON")
    Rel(spa, moderation, "Reports, hides, appeals", "HTTPS/JSON")
    Rel(spa, summary, "Requests summary", "HTTPS/JSON")
    Rel(spa, hub, "Subscribes", "WebSocket")
    Rel(auth, idp, "Verifies identity", "OIDC")
    Rel(posts, policy, "Checks access")
    Rel(drafts, policy, "Checks officer role")
    Rel(moderation, policy, "Checks role")
    Rel(summary, policy, "Filters visible comments")
    Rel(hub, policy, "Filters each event per recipient")
    Rel(posts, hub, "Publishes events")
    Rel(drafts, hub, "Publishes events")
    Rel(moderation, hub, "Publishes events")
    Rel(summary, llm, "summarize()", "HTTPS")
    Rel(posts, repo, "Uses")
    Rel(groups, repo, "Uses")
    Rel(drafts, repo, "Uses")
    Rel(moderation, repo, "Uses")
    Rel(summary, repo, "Uses")
    Rel(repo, db, "SQL", "asyncpg")
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
