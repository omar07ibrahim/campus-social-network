# 1.3 Non-Functional Requirements

> Lead: Salama. Every target is measurable and says how it will be checked in Assignment 2.
> Targets are sized for a pilot at one campus (NFR-2), not for a national-scale service.

| ID | Quality | Measurable target | How it is checked | Why this target | Source |
|---|---|---|---|---|---|
| NFR-1 | Performance | 95% of feed requests (`GET /posts`, 20 posts) answer in < 500 ms with 200 concurrent users | Load test (Locust) before the A2 demo | Feeds slower than ~0.5 s feel broken; 200 concurrent ≈ busiest hour of the pilot | S1 |
| NFR-2 | Scalability | 5,000 accounts, 200 groups, 50,000 posts without schema or architecture change | Seed script + NFR-1 load test on the seeded DB | Roughly the size of the MBZUAI community plus growth; assumption A-2 | S4 |
| NFR-3 | Availability | 99% monthly uptime between 08:00 and 22:00 Gulf time | Uptime check on `/health` every minute | Students use it around classes; nights can host maintenance | S1, S4 |
| NFR-4 | Live updates / moderation speed | A new post or report reaches connected clients within 2 s (p95) | Integration test with two WebSocket clients | Moderators must see reports quickly to limit harm; collaborators must see edits | S2, S3 |
| NFR-5 | Data integrity | 100% of hide/remove/appeal actions produce a durable moderation record in the same transaction | Automated test that kills the request mid-action and checks no half-written state | Decisions without records cannot be appealed or audited | S3 |
| NFR-6 | Accessibility | WCAG 2.1 AA on sign-in, feed, post, comment and draft screens | axe-core in CI plus one manual keyboard-only pass | University digital services are expected to be accessible | S1, S4 |
| NFR-7 | Security | 100% of write endpoints reject unauthenticated or unauthorised requests (401/403); no secrets in the repo or browser bundle | Authorization test matrix (role × endpoint); secret scan in CI | Group-only content and moderator powers are the main attack targets (S5) | S4, S5 |
| NFR-8 | Concurrency correctness | 0 silent overwrites: every stale draft save returns 409 | Test with two clients saving the same draft version | Officers must not lose each other's work (FR-7) | S2 |
| NFR-9 | Recovery | Data loss ≤ 15 minutes (RPO) and service restored within 4 hours (RTO) | Restore drill from backup once before the A2 demo | A lost moderation record or announcement is worse than short downtime | S3, S4 |
| NFR-10 | Privacy | 0 group-only posts returned to non-members; LLM requests contain only comment text and display names; a user's data is deleted within 30 days of a deletion request | Authorization tests; logged LLM payloads reviewed in tests | Students' trust and university data rules | S1, S4 |
| NFR-11 | Usability | 4 of 5 first-time test users create a post and a comment in under 2 minutes without help | Short hallway test with 5 students in A2 | If posting is harder than a chat app, students stay in chat apps | S1 |
| NFR-12 | Auditability | 100% of moderation actions, appeals, role changes and verifications are logged with actor, time and reason, kept 1 year, not editable through the API | Test that each action writes an audit row; no update/delete endpoint exists for it | Appeals and university complaints need a trustworthy history | S3, S4 |

## 2.1 Architectural drivers (ranked)

> Lead: Salama, with technical input from Makar (data, backend) and Omar (frontend, real-time).

| Rank | Driver | How it shaped the design |
|---|---|---|
| 1 | **Audience control & privacy** (FR-4, NFR-7, NFR-10) | All visibility checks live in one backend component (Access Policy, see component diagram) used by REST *and* WebSocket paths; the browser is never trusted to filter. |
| 2 | **Data integrity & auditability** (NFR-5, NFR-12) | Relational database with foreign keys and transactions (ADR-03); moderation records and audit events are append-only rows. |
| 3 | **Concurrent collaboration** (FR-7, NFR-8, NFR-4) | Version-checked draft saves plus a WebSocket channel for presence and change notices (ADR-04), instead of a CRDT engine. |
| 4 | **Trustworthy AI output** (FR-8, FR-15) | Summaries cite comment ids; LLM behind an adapter so a mock can be used and payloads can be tested (ADR-02). |
| 5 | **Performance & scalability** (NFR-1, NFR-2) | Paginated feed, indexed `created_at`/`group_id`; one FastAPI service is enough for the pilot, so no microservices. |
| 6 | **Availability & recovery** (NFR-3, NFR-9) | Managed Postgres backups; stateless API so it can be restarted or duplicated. |
| 7 | **Accessibility & usability** (NFR-6, NFR-11) | Affects frontend component choice (accessible rich-text editor), not the overall structure. |
