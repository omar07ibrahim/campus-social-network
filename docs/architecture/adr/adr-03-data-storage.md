# ADR-03: Data Storage Approach

- **Status:** Accepted
- **Owner:** Makar
- **Date:** 2026-10-05 (first draft 2026-09-29)
- **Feasibility review:** Omar — fine for the frontend, no direct impact beyond the API contract.
- **Related:** NFR-2, NFR-5, NFR-9, NFR-12, ADR-01, ADR-04, `diagrams/er-diagram.md`

## Context
The POC keeps posts in memory. Assignment 2 needs persistent users, groups, memberships,
posts, comments, drafts, reports, moderation records, summaries and an audit log. The data
is strongly linked (post → group → membership → user; moderation record → post → moderator),
and two rules are critical: a moderation decision must never be half-written (NFR-5), and
two officers saving the same draft must not overwrite each other (NFR-8).

## Options considered
1. **Document store (MongoDB)** — flexible schema and quick start, but our data is relational;
   joins, uniqueness ("one report per user per post") and cross-document consistency would
   have to be rebuilt in application code.
2. **SQLite** — zero setup and fine for the POC, but a single writer lock and no managed
   backups make concurrent drafts (ADR-04) and the recovery target (NFR-9) hard.
3. **PostgreSQL** — foreign keys, CHECK and UNIQUE constraints express the policies in
   `er-diagram.md`; transactions make "hide post + write record" atomic; managed hosting gives
   point-in-time recovery; well supported by FastAPI through SQLModel/SQLAlchemy and Alembic.

## Decision
PostgreSQL 16, accessed from FastAPI through SQLModel (SQLAlchemy) with the async `asyncpg`
driver, and Alembic for migrations. Local development runs Postgres in Docker Compose.
Not used in the Assignment 1 POC, which deliberately stays in memory (see `docs/poc.md`).

## Consequences
- **Positive:** Policy rules become database constraints (visibility ⇔ group, second
  moderator ≠ first, unique report), so a bug in one endpoint cannot break them (NFR-5).
- **Positive:** Optimistic locking for drafts is one conditional `UPDATE … WHERE version = ?`
  (ADR-04) — no extra infrastructure.
- **Positive:** Point-in-time recovery on the managed service meets RPO 15 min (NFR-9).
- **Negative:** Every schema change needs a migration and review; slower than a schemaless store.
- **Negative:** Team must run Docker for local development; mitigated by one
  `docker-compose up` command in the A2 README.
- **Follow-up:** If the live feed (NFR-1) gets slow at pilot scale, add read indexes or a
  cache before considering a different store.
