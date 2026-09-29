# C4 — Level 2: Containers

Assignment 2 target architecture. The Assignment 1 POC only implements the Browser SPA
(plain HTML/JS here, not React yet) and the API container (in-memory, not Postgres) —
see README "POC simplifications".

```mermaid
C4Container
    title CampusConnect — Containers (Assignment 2 target)

    Person(student, "Student / Officer / Moderator")

    System_Boundary(campusconnect, "CampusConnect") {
        Container(spa, "Web App", "React + rich text editor", "Feed, drafts, moderation UI")
        Container(api, "Backend API", "FastAPI (Python)", "REST endpoints: posts, comments, moderation, auth")
        Container(ws, "Realtime Gateway", "FastAPI WebSockets", "Live feed updates, draft presence/conflict notices (ADR-04)")
        ContainerDb(db, "Database", "PostgreSQL", "Users, groups, posts, comments, moderation records (ADR-03)")
    }

    System_Ext(llm, "LLM Provider", "Thread summarization (ADR-02)")

    Rel(student, spa, "Uses", "HTTPS, browser")
    Rel(spa, api, "Calls", "HTTPS/JSON — api-contract.md")
    Rel(spa, ws, "Subscribes", "WebSocket")
    Rel(api, db, "Reads/writes", "SQL (SQLAlchemy/SQLModel)")
    Rel(ws, db, "Reads", "SQL")
    Rel(api, llm, "Requests summary", "HTTPS/API")
```

## Assignment 1 POC container view (what actually runs today)

```mermaid
C4Container
    title CampusConnect POC — Containers (Assignment 1, as implemented)

    Person(demo_user, "Demo user")

    System_Boundary(poc, "CampusConnect POC") {
        Container(frontend, "Frontend", "Static HTML + vanilla JS", "frontend/index.html, app.js")
        Container(backend, "Backend", "FastAPI (Python)", "backend/main.py — in-memory list, no DB")
    }

    Rel(demo_user, frontend, "Opens in browser")
    Rel(frontend, backend, "POST/GET /posts", "fetch(), JSON, CORS: *")
```
