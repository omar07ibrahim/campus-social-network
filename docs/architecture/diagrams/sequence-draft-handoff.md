# 2.3 UML Sequence Diagram — Two Officers Co-edit and Publish a Draft

> Lead: Omar, backend steps by Makar. The collaborative interaction required by 2.3:
> officers Salama and Aro of the same group prepare one announcement (FR-7, US-8, ADR-04).

```mermaid
sequenceDiagram
    actor S as Officer Salama (browser)
    actor A as Officer Aro (browser)
    participant API as Backend API (Drafts service)
    participant P as Access Policy
    participant DB as PostgreSQL
    participant HUB as Realtime hub (WebSocket)

    S->>HUB: subscribe draft:42
    HUB->>P: is Salama an officer of the draft's group?
    P-->>HUB: yes
    A->>HUB: subscribe draft:42
    HUB-->>S: draft.presence {viewers: [Salama, Aro]}
    HUB-->>A: draft.presence {viewers: [Salama, Aro]}

    S->>API: GET /drafts/42
    API-->>S: 200 {content, version: 7}
    A->>API: GET /drafts/42
    API-->>A: 200 {content, version: 7}

    Note over S,A: Both edit at the same time, both based on version 7

    S->>API: PUT /drafts/42 {content: S-text, version: 7}
    API->>P: officer check
    API->>DB: UPDATE draft SET content, version=8 WHERE id=42 AND version=7
    DB-->>API: 1 row updated
    API-->>S: 200 {version: 8}
    API->>HUB: draft.updated {version: 8, edited_by: Salama}
    HUB-->>A: draft.updated {version: 8, edited_by: Salama}

    A->>API: PUT /drafts/42 {content: A-text, version: 7}
    API->>DB: UPDATE ... WHERE id=42 AND version=7
    DB-->>API: 0 rows updated (version is now 8)
    API-->>A: 409 version_conflict {current: {content: S-text, version: 8}}
    Note over A: Editor shows both texts side by side, Aro merges

    A->>API: PUT /drafts/42 {content: merged, version: 8}
    API->>DB: UPDATE ... WHERE id=42 AND version=8
    DB-->>API: 1 row updated
    API-->>A: 200 {version: 9}
    API->>HUB: draft.updated {version: 9, edited_by: Aro}
    HUB-->>S: draft.updated {version: 9, edited_by: Aro}

    S->>API: POST /drafts/42/publish {version: 9, visibility: group}
    API->>DB: BEGIN, insert POST, link draft, COMMIT
    alt commit succeeds
        API-->>S: 201 {post}
        API->>HUB: post.created (sent only to group members)
    else database error or timeout
        API-->>S: 503, nothing published
        Note over S: Draft is unchanged (version 9), Salama retries
    end
```

## What happens when users act concurrently
- Both officers can type at the same time; nothing is locked. Saves are checked against the
  version the officer started from. The first save wins; the second gets **409** with the
  current text, so no edit is silently lost (NFR-8).
- Presence events show who else is in the draft, so most conflicts are avoided before they
  happen.
- If both press **Publish** at once, both requests carry version 9: the first creates the
  post and marks the draft published; the second gets 409 (`already published`) — the
  announcement is never posted twice.

## What happens when an operation fails
| Failure | Behaviour |
|---|---|
| WebSocket drops | Client reconnects with backoff and refetches the draft over REST; edits are never sent over the socket, so none are lost |
| Save request times out | Client keeps the text locally and retries with the same version; a duplicate is harmless because the version check rejects it (409 with the same content) |
| Database error during publish | Transaction rolls back; no post exists, draft unchanged, client gets 503 and can retry |
| Officer loses officer role mid-edit | Next save returns 403; the draft stays for the remaining officers |
| Officer opens the editor while offline | Editor is read-only until the latest version is fetched |
