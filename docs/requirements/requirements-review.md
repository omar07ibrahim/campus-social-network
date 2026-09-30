# Requirements Review (1.5)

> Reviewed together 2026-09-29 by Omar, Salama, Makar (Aro joined for user stories, see
> `user-stories.md`). Feasibility checked by Makar and Omar against the POC and A2 architecture.

## Review notes
- FR-1/FR-2 (create/view post) are implemented and tested in the Assignment 1 POC
  (`backend/test_main.py`) — the only requirements with working code so far.
- FR-5/FR-6 (moderation) depend on ADR-01's decision (moderators + group officers) — checked
  against the stakeholder conflict table in `stakeholders.md`, no contradiction found.
- FR-7 (draft hand-off) and NFR-8 (concurrency) are consistent with ADR-04's decision
  (optimistic concurrency + WebSocket presence) — Makar/Omar confirmed this is buildable
  with FastAPI WebSockets in the Assignment 2 timeframe (see `project-management/README.md`).
- FR-9 (group verification) has no owning ADR yet — flagged as an open question below.
- NFR-2's "5,000 students / 200 groups" figure is a placeholder pilot target, not a
  validated number from Student Affairs — flagged as an assumption below.

## Assumptions
- University context is MBZUAI; "campus-verified" means a university email domain check
  (mocked in the POC, real integration is Assignment 2 scope).
- The 5,000-student / 200-group scale (NFR-2) is an assumed pilot size, not confirmed by
  any real stakeholder at MBZUAI.
- Group verification (FR-9) is performed by a human authority (Student Affairs), not
  automated — process itself is out of scope for this assignment.

## Open questions
- Who exactly grants group verification (FR-9) — no ADR owner assigned yet.
- Appeals process detail for moderation decisions (ADR-01, carried over from `user-stories.md`).
- Whether NFR-3's uptime target needs to hold during the 3-minute demo only, or continuously
  through Assignment 2 grading — assumed continuous for now.
