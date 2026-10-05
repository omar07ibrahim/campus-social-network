# Proof-of-Concept Sequence — Create a Post

> Lead: Omar. The single interaction implemented in Assignment 1 (Section 4) and shown in
> the demo. Matches `backend/main.py`, `frontend/app.js` and `api-contract.md` Part A.

```mermaid
sequenceDiagram
    actor U as Student (browser)
    participant FE as Frontend (index.html / app.js)
    participant API as Backend (FastAPI, main.py)

    U->>FE: Fill author + content, click "Post"
    FE->>API: POST /posts {author, content}
    API->>API: Pydantic: trim, check 1-100 / 1-1000 chars
    alt valid
        API->>API: create id (uuid4) + created_at (UTC), append to list
        API-->>FE: 201 {id, author, content, created_at}
        FE-->>U: post added at top of the feed, form cleared
    else missing / empty / too long
        API-->>FE: 422 {detail: [{type, loc, msg, input}]}
        FE-->>U: inline error, e.g. "content: String should have at least 1 character"
    end

    Note over U,API: On page load: GET /posts -> 200 [posts newest first]
```
