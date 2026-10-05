# 2.4 Interfaces

> Lead: Makar (backend), agreed with Omar (frontend) on 2026-09-29 before coding (Step 3 of
> the brief). Part A is implemented and tested in the proof of concept. Part B is the
> Assignment 2 contract the architecture is designed around.

# Part A — Proof-of-concept contract (implemented)

Base URL `http://localhost:8000`. JSON over HTTP. No authentication in the POC.

## POST /posts — create a post

**Request**
```json
{ "author": "Omar", "content": "Study group for AI1220 at 6pm, library room 2" }
```
| Field | Rule |
|---|---|
| `author` | string, required, 1–100 characters after trimming spaces |
| `content` | string, required, 1–1000 characters after trimming spaces |

**201 Created**
```json
{
  "id": "6f1c2a4e-1b7d-4c55-9a0e-2f8f3b9d7c11",
  "author": "Omar",
  "content": "Study group for AI1220 at 6pm, library room 2",
  "created_at": "2026-10-05T09:30:12.123456Z"
}
```

**422 Unprocessable Entity** — missing, empty, whitespace-only or too-long field. Nothing is
stored. This is FastAPI/Pydantic v2's standard shape; the frontend shows `loc[-1]: msg`.
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "content"],
      "msg": "Field required",
      "input": { "author": "Omar" }
    }
  ]
}
```
Other `type` values the POC can return: `string_too_short` (empty/whitespace),
`string_too_long` (> limit), `string_type` (not a string).

## GET /posts — list posts

**200 OK** — array of the post objects above, newest first. `[]` when there are no posts.

## GET /health

**200 OK** — `{ "status": "ok" }`

Verified by `backend/test_main.py` (8 tests) and by the browser demo.

# Part B — Assignment 2 interfaces (planned)

## Authentication and authorization rules
- The browser signs in through the university identity provider (OIDC; a mock provider in
  development). The backend issues a session cookie (`HttpOnly`, `Secure`, `SameSite=Lax`).
  No token is stored in JavaScript.
- Every request except `/health` and the sign-in callback requires a session → otherwise **401**.
- Authorization is decided by the Access Policy component (ADR-01), never by the browser:

| Role | Can |
|---|---|
| `student` | read campus posts and posts of groups they belong to; post, comment, report, appeal own hidden posts, request summaries |
| `officer` (per group) | everything a student can, plus edit that group's drafts, publish as the group, remove posts in that group |
| `moderator` | hide any post, decide appeals on decisions they did not make |
| `student_affairs` | verify groups, grant/revoke moderator role |

## Error format
- **422** keeps FastAPI's validation shape from Part A.
- All other errors: `{ "detail": "<human-readable message>", "code": "<machine code>" }`

| Status | When | Example `code` |
|---|---|---|
| 401 | no or expired session | `not_authenticated` |
| 403 | authenticated but not allowed | `not_group_member`, `not_officer`, `same_moderator` |
| 404 | resource missing **or** not visible to the caller (no existence leak) | `not_found` |
| 409 | stale draft version, duplicate report, second appeal | `version_conflict`, `already_reported`, `appeal_exists` |
| 429 | more than 10 posts or 30 comments per user per minute | `rate_limited` |
| 503 | LLM provider unavailable or timed out (8 s) | `summary_unavailable` |

## REST endpoints

| Method & path | Request body | Success | Who | Failures | FR |
|---|---|---|---|---|---|
| `GET /me` | — | 200 user + roles + memberships | any | 401 | FR-11 |
| `GET /posts?group_id=&before=&limit=20` | — | 200 visible posts, newest first | any | 401, 403 (group not joined) | FR-2, FR-4 |
| `POST /posts` | `{content, visibility: "campus"\|"group", group_id?}` | 201 post | any; `group` needs membership | 401, 403, 422, 429 | FR-1, FR-4 |
| `GET /posts/{id}/comments` | — | 200 comments, oldest first | can see post | 401, 404 | FR-3 |
| `POST /posts/{id}/comments` | `{content}` | 201 comment | can see post | 401, 404, 422, 429 | FR-3 |
| `POST /groups/{id}/members` | — | 201 membership | any | 401, 404, 409 | FR-12 |
| `DELETE /groups/{id}/members/me` | — | 204 | member | 401, 404 | FR-12 |
| `POST /groups/{id}/verify` | — | 200 group | student_affairs | 401, 403 | FR-9 |
| `POST /groups/{id}/drafts` | `{content}` | 201 draft `{id, version: 1}` | officer | 401, 403, 422 | FR-7 |
| `PUT /drafts/{id}` | `{content, version}` | 200 draft with `version + 1` | officer of group | 401, 403, **409 + latest draft** | FR-7 |
| `POST /drafts/{id}/publish` | `{version, visibility}` | 201 post | officer of group | 401, 403, 409 | FR-7 |
| `POST /posts/{id}/reports` | `{reason}` | 201 report | can see post | 401, 404, 409, 422 | FR-10 |
| `POST /posts/{id}/hide` | `{reason}` | 200 moderation record | moderator, or officer of the post's group | 401, 403, 404 | FR-5, FR-6 |
| `POST /moderation/{id}/appeal` | `{statement}` | 201 appeal pending | author of the post | 401, 403, 409 | FR-14 |
| `POST /moderation/{id}/appeal/decision` | `{outcome: "restored"\|"upheld", note}` | 200 | moderator ≠ original decider | 401, 403 (`same_moderator`) | FR-14 |
| `POST /posts/{id}/summary` | — | 200 summary (below) | can see post | 401, 404, 422 (< 20 comments), 503 | FR-8 |
| `POST /summaries/{id}/flag` | `{reason}` | 201 | can see post | 401, 404 | FR-15 |

**409 on a stale draft save** returns the current draft so the client can merge:
```json
{ "detail": "Draft changed since you opened it", "code": "version_conflict",
  "current": { "id": "…", "version": 7, "content": "…", "last_edited_by": "Aro" } }
```

**Summary response**
```json
{
  "id": "…", "post_id": "…", "generated_at": "2026-10-05T10:00:00Z",
  "label": "AI-generated summary — check the linked comments",
  "points": [
    { "text": "Most people prefer Thursday for the meetup.", "source_comment_ids": ["c12", "c19", "c31"] }
  ],
  "comment_count": 54
}
```

## WebSocket events — `wss://…/ws`
The client connects with its session cookie and subscribes; the server sends only events
the user may see (filtered by Access Policy per recipient).

```json
// client → server
{ "type": "subscribe", "channel": "feed" }
{ "type": "subscribe", "channel": "post:<post_id>" }
{ "type": "subscribe", "channel": "draft:<draft_id>" }      // officers of that group only

// server → client
{ "type": "post.created",    "post": { …post… } }
{ "type": "post.hidden",     "post_id": "…" }
{ "type": "comment.created", "post_id": "…", "comment": { …comment… } }
{ "type": "draft.updated",   "draft_id": "…", "version": 8, "edited_by": "Salama" }
{ "type": "draft.presence",  "draft_id": "…", "viewers": ["Salama", "Aro"] }
{ "type": "report.created",  "post_id": "…" }                 // moderators only
{ "type": "error", "code": "forbidden_channel" }
```
Live events are notifications only. Writes always go through REST, so validation and
authorization live in one place. After a reconnect the client refetches over REST, so a
missed event never leaves stale data on screen.

## External service — LLM provider (behind the Summary adapter)
```
summarize(comments: list[{id, author_display_name, text}]) -> list[{text, source_comment_ids}]
```
- Implementations: `MockSummarizer` (dev/tests, deterministic) and a real provider client.
- Timeout 8 s, one retry, then 503 `summary_unavailable` to the client.
- Points that cite no comment id, or an id that was not in the input, are dropped before
  the response is returned (ADR-02).
- The API key lives only in the backend's environment (see `repository-structure.md`).
