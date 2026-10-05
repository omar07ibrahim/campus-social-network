# Project Management

> Lead: Aro. Drafted by the team 2026-09-29, based on this repo's actual Git workflow and
> the assignment brief. Aro owns final wording and risk assessment.

## Responsibilities
| Member | Lead role |
|---|---|
| Salama | Requirements & product scope (1.1–1.3, 2.1) |
| Aro | Planning, validation, report (1.4–1.5, Section 3) |
| Makar | Backend & data architecture (2.4–2.6) |
| Omar | Frontend & integration (2.2–2.3) |

Each person writes their own lead sections; Aro assembles the final report (per assignment brief).

## Git workflow
- Single shared repo: `omar07ibrahim/campus-social-network` (private, teaching team added
  as a read collaborator).
- `master` is the working branch for Assignment 1 (small team, short timeline); Assignment 2
  moves to feature branches + PR review once the codebase is large enough to need it
  (see risk R2 below).
- Commit convention: imperative subject line, author set to whoever actually wrote the
  content (`Co-authored-by:` trailer when more than one person contributed to a commit).

## Development approach
Lightweight, milestone-driven — not full Scrum (team is 4 people, project is 2 assignments,
not a multi-sprint product). Work is grouped by assignment deliverable (requirements →
architecture → PM → POC), agreed together at the start (Step 1–3 of the assignment's
suggested order), then built in parallel with a review pass before submission.

## Risks
| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| R1: Requirements/architecture drift apart (docs say one thing, code does another) | Medium | High | `api-contract.md` is the single source of truth for request/response shape; both sides tested against it (see `backend/test_main.py`) |
| R2: `master`-only workflow breaks down once Assignment 2 has real concurrent backend/frontend work | Medium | Medium | Move to feature branches + PR review at the start of Assignment 2, before the codebase grows |
| R3: One member (Aro) blocked on the others' sections for the final report | Low | High | Each lead section is its own file under `docs/`, written independently; Aro assembles, doesn't wait to start until everyone else finishes |
| R4: AI feature (thread summarization, ADR-02) scoped too ambitiously for Assignment 2's timeline | Medium | Medium | POC explicitly excludes AI integration (see README); Assignment 2 can start with a stubbed/mocked summary before wiring a real LLM call |
| R5: Oral exam — a member can't explain a part they didn't personally write | Medium | High | Step 6 of the assignment brief: practice session where each member explains every section, not just their own |
| R6: Appeals process (ADR-01) assumes ≥2 active campus moderators; if only 1 exists, appeals can't be reviewed by a second person | Low | Medium | Flagged in `requirements-review.md`; Assignment 2 can fall back to admin review if moderator pool is 1 |
| R7: Two collaborator invites (Makar, Teaching Team/prof) still pending acceptance on GitHub as of 2026-10-05 | Medium | High | Follow up directly — repo access for the teaching team is a hard submission requirement (final checklist) |

## Assignment 2 timeline
_(Placeholder milestones — Aro/team to confirm real dates against the course schedule.)_

| Milestone | Target |
|---|---|
| Data model + Postgres schema live (ADR-03) | Week 1 |
| FastAPI backend: auth (mocked), posts, comments, moderation | Week 2–3 |
| React frontend, rich text editor | Week 2–3 (parallel with backend) |
| WebSocket live updates + draft-editing concurrency (ADR-04) | Week 4 |
| AI feature: thread summarization (ADR-02) | Week 4–5 |
| Integration testing, demo prep, report assembly | Week 5–6 |
