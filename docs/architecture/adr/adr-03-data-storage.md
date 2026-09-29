# ADR-03: Data Storage Approach

- Status: draft (owner Makar — final wording still to review)
- Owner: Makar
- Date: 2026-09-29

## Context
The Assignment 1 POC keeps posts in memory (see README, "explicitly excluded"). Assignment 2
needs real persistence for: users, groups, posts, comments, RSVPs/attendance, and moderation
records (report → hide → decision, ADR-01) that must survive restarts and support appeals.
Entities are clearly relational: a post belongs to a group and an author, a moderation record
references a post and a moderator, a comment references a post and an author.

## Alternatives considered
1. **Document store (e.g. MongoDB)** — flexible schema, easy to start, but the data is
   inherently relational (foreign keys everywhere: post→group, post→author, moderation
   record→post→moderator) and we'd rebuild joins/consistency checks in application code.
2. **SQLite** — zero ops, fine for the POC, but not realistic for Assignment 2's multi-user,
   concurrent-write scenario (ADR-04) or for demonstrating a production-plausible architecture.
3. **PostgreSQL (relational)** — native foreign keys and constraints match the data model
   directly; transactions give ACID guarantees for moderation decision records (can't lose a
   decision mid-write); mature FastAPI support (SQLAlchemy/SQLModel + Alembic migrations).

## Decision
Option 3: PostgreSQL, accessed via SQLAlchemy/SQLModel from FastAPI, with Alembic for schema
migrations. Not implemented in the Assignment 1 POC (in-memory only, see README); this ADR
governs the Assignment 2 backend.

## Consequences
- Requires running/hosting a Postgres instance (local Docker container for dev, per Assignment 2).
- Relational constraints (foreign keys, NOT NULL, unique) enforce data integrity that would
  otherwise be re-implemented manually in a document store.
- Schema changes need migrations (Alembic) — more process than a schemaless store, but this
  is the right trade-off given moderation/appeal records must not silently lose fields.
- Sets the ER diagram (2.6) and repository structure (2.5) to be table/model-based, not
  document-collection-based — Makar to keep this consistent across those sections.
