# Non-Functional Requirements

> Lead: Salama (1.3), architectural drivers ranked with technical input from Makar and Omar
> (2.1). Each target is measurable — a vague "fast" or "secure" is not acceptable here.

| ID | Category | Requirement | Measurable target | Source / driver |
|---|---|---|---|---|
| NFR-1 | Performance | Feed loads quickly under normal load | 95% of `GET /posts` requests return in < 500ms at up to 200 concurrent users | S1 (usability) |
| NFR-2 | Scalability | Supports a pilot campus population | 5,000 students, 200 groups, without redesign (informed by earlier individual CampusPulse analysis) | S4 |
| NFR-3 | Availability | Usable during class hours | 99% uptime, 8am–10pm campus time, during Assignment 2 demo period | S1, S4 |
| NFR-4 | Moderation SLA | Reports are actionable quickly enough to limit harm | A report is visible to a moderator within 1 minute (near-real-time via WebSocket, ADR-04 infra) | S3 |
| NFR-5 | Data integrity | Moderation decisions are never silently lost | 100% of hide/remove actions produce a durable `MODERATION_RECORD` row (ADR-01, ADR-03) — verified by test, not just code review | S3 |
| NFR-6 | Accessibility | Usable with assistive tech | WCAG 2.1 AA on the core feed/post/comment flows | S1 |
| NFR-7 | Security (A2) | Only verified university accounts can post | 100% of posts have a non-null `author_id` linked to a university-verified account; POC/Assignment 1 explicitly mocks this (see README) | S4 |
| NFR-8 | Concurrency correctness | No silent draft overwrite between two officers | Version-conflict rate observable and rejected writes return 409, not silent overwrite (ADR-04) — verified by test in Assignment 2 | S2, S3 |

## Architectural drivers ranking (2.1)

Ranked by the team, with technical feasibility input from Makar and Omar:

1. **Data integrity (NFR-5)** — moderation records must never silently disappear; drives
   PostgreSQL choice (ADR-03) over a less strict store.
2. **Concurrency correctness (NFR-8)** — draft hand-off must not lose officer work; drives
   optimistic-concurrency + WebSocket design (ADR-04).
3. **Performance (NFR-1)** — feed responsiveness is what students actually notice; drives
   keeping the POC/A2 read path simple (no heavy joins on the hot path).
4. **Scalability (NFR-2)** and **Availability (NFR-3)** — real but secondary at pilot scale;
   informs choosing Postgres (scales further than SQLite) without over-engineering for the
   POC/early Assignment 2 stage.
5. **Accessibility (NFR-6)** and **Security (NFR-7)** — required for release, but not decided
   by an ADR in this assignment; flagged as Assignment 2 implementation requirements.
