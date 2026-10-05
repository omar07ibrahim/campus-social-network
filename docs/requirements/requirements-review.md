# 1.5 Validation and Traceability

> Lead: Aro. Feasibility checked by Makar and Omar; requirement wording owned by Salama.

## How we reviewed the requirements
1. **Scope walkthrough (2026-09-29, all four):** agreed users, features, visibility rules,
   moderation policy and AI feature before writing anything (Step 1 of the brief).
2. **Checklist per requirement:** for every FR/NFR we asked: Is it observable behaviour? Can
   it be tested, and how? Which stakeholder needs it? Is it a requirement or a design choice?
   Does it conflict with another requirement? Vague words ("fast", "secure", "quickly") were
   replaced by numbers.
3. **Feasibility check (Makar, Omar):** each requirement mapped to a component in
   `diagrams/c4-component.md` and to an endpoint or event in `api-contract.md`.
4. **Consistency review (2026-10-05):** compared requirements, diagrams, contract, ADRs and the
   running POC side by side (Step 5 of the brief). Findings below.

## Contradictions and unclear wording we resolved
| # | Problem found | Resolution |
|---|---|---|
| R-1 | ER diagram used visibility `public`, ADR-01 said "campus-wide" | One vocabulary everywhere: `campus` / `group` |
| R-2 | Scope listed live updates and rich text as *future*, but Assignment 2 requires them and NFR-4 depends on WebSockets | Moved into the first release (`scope.md`) |
| R-3 | ADR-01 requires appeals, but the ER model had no field for them | `appeal_*` fields and a CHECK (second moderator ≠ first) added to `MODERATION_RECORD` |
| R-4 | NFR-4 said reports reach moderators "within 1 minute" while the design pushes them live | Single target: live events within 2 s (p95) |
| R-5 | FR-9 (group verification) had no story and no owner | US-7 added; policy owned by ADR-01 |
| R-6 | "Group" and "officer" were undefined | Defined through `GROUP_MEMBERSHIP` with role `member` / `officer` |
| R-7 | US-1 says empty posts are rejected, but the POC accepted content of only spaces | Backend trims before validating; test added |
| R-8 | No requirement covered identity, joining groups, live updates or appeals, though the brief lists them | FR-11 … FR-15 and US-8 … US-10 added |

## Assumptions
| ID | Assumption | If wrong |
|---|---|---|
| A-1 | University context is MBZUAI; a valid account is an `@mbzuai.ac.ae` address from the university identity provider | Change the domain list in Auth config |
| A-2 | Pilot size ≈ 5,000 accounts and 200 groups (NFR-2); not confirmed by Student Affairs | Re-run load test with the real figure |
| A-3 | At least two active moderators at any time (appeals, ADR-01) | Appeals escalate to Student Affairs (R6) |
| A-4 | Group verification is a manual decision by Student Affairs | — |
| A-5 | A free or mock LLM is acceptable for Assignment 2 (brief: paid calls not required) | Adapter allows another provider |
| A-6 | Sending comment text and display names to the LLM provider is acceptable to the university if nothing is retained by the provider | Switch to a self-hosted model behind the same adapter |

## Open questions
| ID | Question | Who decides |
|---|---|---|
| Q-1 | Must the 99% availability target (NFR-3) hold during grading, or only during the demo? Assumed: during the Assignment 2 demo period | Teaching team |
| Q-2 | How is the first Student Affairs account created? Planned: a seed script run by an admin, not an API endpoint | Team (Makar) in A2 |
| Q-3 | Can students report anonymously to the author? Planned: reporter is hidden from the author, visible to moderators | Student Affairs |
| Q-4 | How long are hidden posts kept after an appeal is decided? Assumed: 1 year with the audit log (NFR-12) | Student Affairs |

## Traceability matrix

Stakeholders: `stakeholders.md` · Requirements: `functional-requirements.md`,
`non-functional-requirements.md` · Stories: `user-stories.md` · Components:
`diagrams/c4-component.md` · ADRs: `adr/`.

| Stakeholder need | FR | NFR | Story | Architecture components | ADR | Verified by |
|---|---|---|---|---|---|---|
| S4, S5: only real university members | FR-11 | NFR-7 | US-1 | Auth, University sign-in | ADR-01 | API auth tests (A2) |
| S1: share an update | FR-1 | NFR-1, NFR-11 | US-1 | Web App, Posts & Comments router, Repositories | — | **POC:** `test_create_post`, `test_whitespace_only_content_returns_422`, `test_content_over_1000_chars_returns_422`, browser demo |
| S1: see what is happening | FR-2 | NFR-1, NFR-2 | US-2 | Posts & Comments router, Repositories | ADR-03 | **POC:** `test_list_posts_newest_first`, `test_list_posts_empty`; load test (A2) |
| S1: discuss posts | FR-3 | NFR-1 | US-5 | Posts & Comments router | — | API tests (A2) |
| S1, S2: control who sees content | FR-4 | NFR-10 | US-6 | Access Policy, Realtime hub, Repositories | ADR-01 | Role × endpoint matrix (A2) |
| S1, S2: belong to communities | FR-12 | NFR-10 | US-6 | Groups router, Access Policy | ADR-01 | API tests (A2) |
| S4: trusted official groups | FR-9 | NFR-12 | US-7 | Groups router, Access Policy | ADR-01 | API tests (A2) |
| S2: prepare announcements together | FR-7 | NFR-8, NFR-4 | US-8 | Drafts service, Realtime hub, Database | ADR-04, ADR-03 | Two-client conflict test (A2) |
| S1, S2: see changes without reloading | FR-13 | NFR-4 | US-5 | Realtime hub, Access Policy | ADR-04 | Two WebSocket client test (A2) |
| S3: act on harmful posts | FR-10, FR-5 | NFR-4, NFR-5, NFR-12 | US-3 | Moderation service, Realtime hub, Database | ADR-01, ADR-03 | Transaction test (A2) |
| S2, S3: officers manage own group | FR-6 | NFR-5, NFR-7 | US-4 | Moderation service, Access Policy | ADR-01 | Role × endpoint matrix (A2) |
| S1, S3: fair decisions | FR-14 | NFR-12 | US-10 | Moderation service, Database CHECK | ADR-01 | API tests (A2) |
| S1: catch up on long threads | FR-8 | NFR-10 | US-9 | Summary service, LLM Provider, Access Policy | ADR-02 | `MockSummarizer` tests (A2) |
| S1, S4: AI output can be checked | FR-15 | NFR-12 | US-9 | Summary service, Web App summary panel | ADR-02 | Citation-check tests (A2) |
| S3, S4: recover from failures | — | NFR-3, NFR-9 | — | Database backups, stateless API | ADR-03 | Restore drill (A2) |
| S1, S4: accessible to all students | — | NFR-6 | — | Web App | — | axe-core in CI (A2) |

Every FR has at least one story; every story traces to at least one FR, component and
verification method.
