# 3 Project Management and Team Collaboration

> Lead: Aro, with input from all members.

## 3.1 Team structure

| Member | Responsibilities | Code/docs they maintain | Backup reviewer |
|---|---|---|---|
| Salama | Product scope, requirements (1.1–1.3), architectural drivers (2.1), ADR-01; in A2: acceptance of each feature against its FRs, access-policy rules | `docs/requirements/` (except stories), `adr-01` | Aro |
| Aro | User stories, validation & traceability (1.4–1.5), project plan (3), ADR-02, report assembly; in A2: test plan, AI summary feature UX, release checklist | `docs/requirements/user-stories.md`, `requirements-review.md`, `docs/project-management/`, `adr-02`, `docs/build_report.py` | Salama |
| Makar | POC backend, interfaces (2.4), repository structure (2.5), data model (2.6), component diagram, ADR-03; in A2: FastAPI services, database, migrations, Access Policy, WebSocket hub | `backend/`, `api-contract.md`, `er-diagram.md`, `c4-component.md`, `adr-03` | Omar |
| Omar | POC frontend, C4 context/container (2.2), behaviour & sequence (2.3), README, demo, ADR-04; in A2: React app, rich-text and draft editor, realtime client, end-to-end tests | `frontend/`, `README.md`, `c4-context.md`, `c4-container.md`, `behaviour-and-design.md`, sequence diagrams, `adr-04` | Makar |

`.github/CODEOWNERS` encodes this table, so GitHub asks the right person to review.

**Coordinating changes across areas.** The API contract is the boundary between Makar's and
Omar's work: any change to it is a pull request reviewed by both, and in A2 the frontend
client is generated from `openapi.json`, so a mismatch breaks the build. A requirement change
touches Salama's or Aro's files and must update the traceability matrix in the same PR.

**Sharing knowledge.** Every member must be able to defend the whole submission. Each
reviewer of a PR must be able to explain it; a weekly 30-minute sync walks through what
changed; before the oral exam each member presents a section they did not write and the
others question them (Step 6 of the brief).

## 3.2 Development workflow

- **Assignment 1 (honest record):** small team, documents mostly, so commits went directly to
  `master`, each authored by the person responsible for that section. Reviews happened in
  person and in team chat.
- **Assignment 2 branches:** `master` is always runnable and protected. Work happens on
  short-lived branches `feat/<area>-<topic>`, `fix/…`, `docs/…`, merged within a few days.
- **Pull requests:** every change goes through a PR linked to an issue. At least one approval
  from the CODEOWNER of the touched area; changes to `api-contract.md`/`openapi.json` need
  both Makar and Omar. CI (tests, lint, secret scan) must pass. Squash-merge with an
  imperative message.
- **Code review checklist:** matches the contract? tests added? authorization handled in the
  Access Policy, not ad hoc? requirement IDs referenced? docs updated?
- **Issues and task tracking:** GitHub Issues, one per user story or technical task, labelled
  by area (`backend`, `frontend`, `docs`) and requirement ID (`FR-7`). A GitHub Projects board
  with columns Backlog → This week → In progress → Review → Done.
- **Recording decisions and requirement changes:** architecture decisions as new or
  superseding ADRs in `docs/architecture/adr/`; requirement changes as PRs that edit the
  requirement, keep its ID (or retire it, never reuse), and update the traceability matrix.
  The Git history is the change log.
- **AI development tools:** we used AI assistants (Claude Code) to draft parts of the
  documents, code and tests in Assignment 1, and will continue in Assignment 2. Rules:
  AI output is committed only by the member who owns that area and who has read and
  understood it; it goes through the same PR review and CI as any code; generated code must
  come with tests that the member has run; no secrets or personal data are pasted into AI
  tools; anything a member cannot explain in the oral exam is rewritten or removed.

## 3.3 Development approach

**Kanban with one-week iterations.** We chose it over Scrum because we are four students
with uneven weekly availability around other courses; fixed sprint commitments and
ceremonies would cost more than they return. Kanban keeps work visible and limits
work-in-progress (max 2 cards per person), while the weekly cycle gives us regular
checkpoints.

- **Iterations:** each week starts with a 30-minute planning sync (pick cards for the week
  from the backlog) and ends with a demo of what works on `master`.
- **Prioritisation:** MoSCoW from `functional-requirements.md` — all *Must* stories before
  *Should*; within that, the architectural drivers (2.1) first, because they are the hardest
  to change later (Access Policy, data model, draft concurrency).
- **Feedback:** weekly demo inside the team; Salama and Aro check finished stories against
  acceptance criteria; feedback from the teaching team is turned into issues; a hallway
  test with 5 students for NFR-11 in week 5.
- **Testing, documentation and technical tasks:** a story is *Done* only when its tests pass
  in CI and its docs/contract are updated — testing and docs are part of each card, not a
  phase at the end. Technical tasks (CI, Docker, migrations) are cards on the same board,
  scheduled in week 1 so feature work is not blocked.

## 3.4 Risks

| ID | Risk | Likelihood | Impact | Reduce it | If it happens |
|---|---|---|---|---|---|
| R1 | Docs, contract and code drift apart | Medium | High | Contract-first; `openapi.json` generated client; PR checklist; traceability updated in the same PR | Week-6 consistency review fixes the report, not the code, where the code is right |
| R2 | Group-only content leaks through one endpoint or live event | Medium | High | One Access Policy used by REST, WebSocket and Summary paths; role × endpoint test matrix | Hotfix, add the missing test case, audit logs for affected posts |
| R3 | LLM gives wrong or misleading summaries | High | Medium | Citations required, uncited points dropped, label + flag button (ADR-02) | Raise threshold, hide feature behind a flag, keep the rest of the app working |
| R4 | LLM provider unavailable, rate-limited or not free | Medium | Medium | Adapter + `MockSummarizer`; demo can run on the mock | Switch provider or demo with the mock and explain |
| R5 | WebSocket and draft-conflict logic takes longer than planned | Medium | High | Start in week 3 with presence + 409 only (no CRDT, ADR-04); two-client tests early | Ship conflict detection without presence; presence is a *Should* |
| R6 | Fewer than two moderators available, so appeals stall | Low | Medium | Assumption A-3 recorded | Appeals escalate to Student Affairs |
| R7 | A member is unavailable for a week (exams, illness) | Medium | Medium | Backup reviewer per area (3.1); small cards; knowledge-sharing sync | Backup picks up the area; scope cut by MoSCoW *Should* items |
| R8 | A member cannot explain a part they did not write in the oral exam | Medium | High | Cross-presentation practice before the exam; AI-tool rule in 3.2 | Extra practice session on weak sections |
| R9 | Secret (LLM key, DB password) committed to Git | Low | High | `.env` ignored, `.env.example` only, gitleaks in CI | Rotate the key immediately, then clean history |

## 3.5 Assignment 2 timeline

Week numbers count from the Assignment 2 release. Each milestone is shown in the weekly demo
and checked by the listed test.

| Week | Milestone — what will work | How we verify it |
|---|---|---|
| 1 | Docker Compose starts API + Postgres + mock sign-in; a user signs in with a university email, a non-university email is rejected; CI runs on every PR | `docker compose up`, sign-in demo, auth tests green |
| 2 | Users create and list posts stored in Postgres; join/leave groups; group-only posts hidden from non-members by REST | Role × endpoint tests for FR-1, FR-2, FR-4, FR-12 |
| 3 | React app with rich-text post editor and comments; feed and comments update live in a second browser without reload | Playwright test with two browser contexts (FR-3, FR-13, NFR-4) |
| 4 | Two officers edit one draft: presence list visible, stale save gets 409 with merge view, publish creates one post | Two-client conflict test (FR-7, NFR-8) |
| 5 | Report → live moderation queue → hide → appeal decided by a second moderator; audit rows written. Usability hallway test (5 students) | Transaction + CHECK tests (FR-5, FR-6, FR-10, FR-14, NFR-5, NFR-12); NFR-11 result |
| 6 | Thread summaries with clickable citations and flagging (mock and real provider); load test and restore drill done; report and demo final | Citation tests (FR-8, FR-15); Locust report (NFR-1); restore log (NFR-9) |
