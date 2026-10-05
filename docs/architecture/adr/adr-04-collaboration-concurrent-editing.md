# ADR-04: Collaboration and Concurrent Editing Approach

- **Status:** Accepted
- **Owner:** Omar
- **Date:** 2026-10-05 (first draft 2026-09-29)
- **Feasibility review:** Makar — conditional UPDATE on a version column is straightforward
  in PostgreSQL/SQLModel (ADR-03).
- **Related:** FR-7, FR-13, NFR-4, NFR-8, US-8, `diagrams/sequence-draft-handoff.md`

## Context
Group officers prepare announcements together and hand drafts to each other before
publishing (S2). Two officers may edit the same draft at the same time. Assignment 2 must use
WebSockets and a React rich-text editor, so the decision should not block live co-editing
later, but it must be buildable and testable by a team of four within Assignment 2.

## Options considered
1. **Pessimistic locking** — one officer checks out a draft, the others are read-only.
   Simple, but a forgotten checkout blocks the group and there is no presence information.
2. **Real-time co-editing with a CRDT/OT library (e.g. Yjs)** — best experience, but adds a
   sync server, binary document state and hard-to-test merge behaviour; overkill for handing
   off announcements.
3. **Optimistic concurrency + WebSocket presence** — each draft has a `version`. A save must
   name the version it was based on; if the draft moved on, the save gets 409 with the latest
   text. A WebSocket channel shows who is viewing and announces each new version.

## Decision
Option 3. Saves go through REST (`PUT /drafts/{id}` with `version`), checked by a
conditional `UPDATE … WHERE version = ?`. The Realtime hub sends `draft.presence` and
`draft.updated` events to officers of that group only. Not part of the Assignment 1 POC.

## Consequences
- **Positive:** No edit is silently overwritten (NFR-8); the rule is one SQL statement and
  easy to test with two clients.
- **Positive:** Presence and update events make conflicts rare and visible.
- **Positive:** The WebSocket channel is reused for the live feed and moderation queue (FR-13).
- **Negative:** On conflict the officer merges by hand; two people cannot type in the same
  paragraph at once.
- **Negative:** The rich-text editor must show a side-by-side merge view — extra frontend work.
- **Later:** If simultaneous typing becomes a real need, Option 2 can replace the draft
  editor only; the REST contract for publishing stays the same.
