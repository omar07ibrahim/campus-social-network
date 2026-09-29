# ADR-04: Collaboration and Concurrent Editing Approach

- Status: draft (owner Omar — final wording still to review)
- Owner: Omar
- Date: 2026-09-29

## Context
Group officers hand off draft posts to each other before publishing (US-4, scope.md). Two
officers may open the same draft around the same time. Assignment 2 must also account for
WebSockets and a React rich-text editor, so this decision should not paint us into a corner
that can't grow into live co-editing later.

## Alternatives considered
1. **Pessimistic locking** — one officer "checks out" a draft; others get a read-only view
   until it's released. Simple, but a forgotten checkout blocks the whole group, and it gives
   no live-presence signal (who else is looking at this draft right now).
2. **Real-time collaborative editing** (WebSocket-synced, CRDT/OT, Google-Docs-style) — best
   UX, but full CRDT/OT is significant scope for a two-assignment project and overkill for
   the actual use case (handing off a draft, not simultaneous live typing by many people).
3. **Optimistic concurrency with a version field** — each draft has a `version` integer;
   saving/publishing requires the client's last-seen version to still match, otherwise the
   save is rejected with a 409 and the officer sees a conflict warning with the latest content
   to merge manually. A WebSocket channel broadcasts "draft updated" / "officer X is viewing"
   presence events so conflicts are rare in practice, without needing full CRDT merge logic.

## Decision
Option 3: optimistic concurrency (version-checked writes) plus a WebSocket presence/notify
channel. This is implemented in Assignment 2, not in the Assignment 1 POC (which has no
draft hand-off at all — POC posts are single-author, published immediately, see scope.md
"Explicitly excluded").

## Consequences
- Officers rarely lose work: conflicts are detected, not silently overwritten.
- Requires the backend to store a `version` per draft and reject stale writes (409) — a real
  API contract detail to nail down in Assignment 2, not just a UI nicety.
- Simpler to build and reason about than true CRDT-based co-editing; trade-off is that two
  officers cannot literally type in the same draft at the same character position at the same
  time — acceptable for this use case (hand-off, not live pair-writing).
- The WebSocket presence channel is reusable for other Assignment 2 features (e.g. "X is
  typing" on comments), so this isn't throwaway infrastructure.
