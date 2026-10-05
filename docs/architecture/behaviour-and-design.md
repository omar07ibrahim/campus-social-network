# 2.3 Behaviour and Design Decisions

> Lead: Omar (coordination, frontend), backend details by Makar. Component names refer to
> `diagrams/c4-component.md`; the collaborative sequence diagram is
> `diagrams/sequence-draft-handoff.md`.

## Audience and authorization rules
- Each post is `campus` or `group` (ADR-01). The **Access Policy** component decides every
  read and write; routers, the Realtime hub and the Summary service all call it.
- Feed queries filter in SQL by the caller's memberships, so hidden or group-only rows never
  leave the database for the wrong user. A post the caller may not see returns **404**, not
  403, so its existence is not revealed.
- The frontend hides buttons a user cannot use, but this is convenience only; the backend
  rechecks everything (NFR-7).

## Publishing and collaboration
- Students publish directly: `POST /posts` validates (Pydantic), stores, then notifies the hub.
- Officers prepare group announcements as shared **drafts**. Saves carry a version number;
  stale saves get **409** with the latest text to merge (ADR-04, sequence diagram).
  Publishing is a single transaction that creates the post and closes the draft.

## Live updates
- One WebSocket per browser tab. Clients subscribe to `feed`, `post:<id>` or `draft:<id>`.
- After any successful write, the service publishes an event to the hub; the hub asks the
  Access Policy for each subscriber before sending, so live events obey the same rules as REST.
- Events are notifications, not the source of truth: on reconnect the client refetches over
  REST. This keeps writes, validation and authorization in one place.

## Moderation and appeals
- Any user can report a post once (FR-10). Reports are pushed live to moderators (NFR-4).
- A moderator (any post) or officer (own group) hides/removes a post. The status change, the
  `MODERATION_RECORD` and an `AUDIT_EVENT` are written in one transaction (NFR-5, NFR-12).
  Content is kept, not deleted.
- The author can appeal once; a *different* moderator decides (database CHECK enforces it).
  Restored posts reappear in feeds through a normal `post.created`-style event.

## AI feature
- On request, for threads with ≥ 20 comments, the **Summary service** collects only the
  comments the requester can see, sends id + display name + text to the LLM adapter, and
  asks for points that each cite comment ids (ADR-02).
- Points without valid citations are dropped. The UI labels the result as AI-generated,
  links each point to its comments, and offers "flag as wrong" (FR-15).
- Summaries are stored with the comment count; when the thread grows by 10+ comments the UI
  offers to regenerate.

## Responsibility for each behaviour
| Behaviour | Responsible part |
|---|---|
| Input validation (lengths, required fields) | Backend routers (Pydantic); browser checks are only for convenience |
| Sign-in, session | Auth component + university identity provider |
| Who can see / do what | Access Policy |
| Draft conflict detection | Drafts service + database conditional UPDATE |
| Pushing live changes | Realtime hub |
| Moderation records, appeals, audit | Moderation service, database transaction |
| Building and checking summaries | Summary service; LLM provider only generates text |
| Rendering rich text safely | Frontend editor + backend sanitising stored HTML/JSON |

## Failures we planned for
| Failure | Planned response | Requirement |
|---|---|---|
| LLM slow, down or returns uncited text | 8 s timeout, one retry, then 503 "summary unavailable"; uncited points dropped; rest of the app unaffected | FR-8, FR-15 |
| WebSocket disconnect | Reconnect with backoff, refetch over REST | FR-13, NFR-4 |
| Two officers save the same draft | 409 with latest content, manual merge | NFR-8 |
| Database unavailable | API returns 503; `/health` reports it; restore from backups within RTO | NFR-3, NFR-9 |
| Crash in the middle of a moderation action | Transaction rolls back, no half-written decision | NFR-5 |
| Spam / flooding | Rate limit 10 posts/min per user (429), report flow | S5 |
| Script injection in posts | Frontend renders text, never raw HTML; rich text sanitised server-side | NFR-7 |
| Only one moderator available for an appeal | Appeal escalates to Student Affairs | R6, ADR-01 |

## Trade-offs
- **Optimistic versions instead of a CRDT** (ADR-04): far simpler and testable, but two
  people cannot type in the same sentence simultaneously; acceptable for announcement drafts.
- **One FastAPI service instead of microservices**: simpler to build and debug for 4 people;
  limit is horizontal scaling of WebSockets, solvable later with Redis pub/sub.
- **Publish-then-moderate**: fast for students (S1), but harmful content can be visible until
  reported; mitigated by live report delivery and the moderation target (NFR-4).
- **Summaries on request, not automatic**: lower LLM cost and less unsolicited AI text, but
  users must click once.

## Developing and testing components separately, and together
- **Contract first:** the API contract (2.4) is agreed before coding; FastAPI's `openapi.json`
  is exported and the frontend client is generated from it, so contract drift fails the build.
- **Separately:** backend unit tests mock the database and the LLM adapter (`MockSummarizer`);
  Access Policy has its own role × resource test table; frontend components are tested
  against a mocked API client.
- **Together:** API tests run against a real Postgres in Docker; Playwright end-to-end tests
  drive the real frontend and backend, including two browser contexts for the draft conflict.
- **Already in Assignment 1:** `backend/test_main.py` (8 tests) checks the POC contract, and
  the create-post flow was checked end-to-end in a real browser.
