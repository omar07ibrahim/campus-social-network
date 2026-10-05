# Requirements Review (1.5)

> Reviewed together 2026-09-29 by Omar, Salama, Makar (Aro joined for user stories, see
> `user-stories.md`). Feasibility checked by Makar and Omar against the POC and A2 architecture.
> Re-reviewed 2026-10-05: appeals process and FR-9 ownership resolved, see below.

## Review notes
- FR-1/FR-2 (create/view post) are implemented and tested in the Assignment 1 POC
  (`backend/test_main.py`) — the only requirements with working code so far.
- FR-5/FR-6 (moderation) depend on ADR-01's decision (moderators + group officers) — checked
  against the stakeholder conflict table in `stakeholders.md`, no contradiction found.
- FR-7 (draft hand-off) and NFR-8 (concurrency) are consistent with ADR-04's decision
  (optimistic concurrency + WebSocket presence) — Makar/Omar confirmed this is buildable
  with FastAPI WebSockets in the Assignment 2 timeframe (see `project-management/README.md`).
- FR-9 (group verification) now folds into ADR-01's policy (updated 2026-10-05) rather than
  getting its own ADR — Student Affairs role grants the badge; no separate decision needed.
- NFR-2's "5,000 students / 200 groups" figure is a placeholder pilot target, not a
  validated number from Student Affairs — flagged as an assumption below.
- Appeals process (resolved 2026-10-05, ADR-01): author requests review, a second moderator
  decides. This assumes ≥2 active moderators — now tracked as a risk, see
  `project-management/README.md` R6.

## Assumptions
- University context is MBZUAI; "campus-verified" means a university email domain check
  (mocked in the POC, real integration is Assignment 2 scope).
- The 5,000-student / 200-group scale (NFR-2) is an assumed pilot size, not confirmed by
  any real stakeholder at MBZUAI.
- Group verification (FR-9) is performed by a human authority (Student Affairs), not
  automated — process itself is out of scope for this assignment.
- Appeals review assumes at least 2 active campus moderators exist at any time (ADR-01) —
  not validated against real staffing.

## Open questions
- Whether NFR-3's uptime target needs to hold during the 3-minute demo only, or continuously
  through Assignment 2 grading — assumed continuous for now.
- Who grants the Student Affairs role itself in the system (bootstrapping problem, carried
  over from `user-stories.md` US-7) — not specified.
