# ADR-01: Audience Visibility and Access-Control Policy

- **Status:** Accepted
- **Owner:** Salama
- **Date:** 2026-10-05 (first draft 2026-09-29)
- **Feasibility review:** Makar (backend), Omar (frontend) — buildable in FastAPI as one
  policy module; no objections.
- **Related:** FR-4, FR-5, FR-6, FR-9, FR-12, FR-14, NFR-7, NFR-10, NFR-12, US-3, US-4, US-6, US-7, US-10

## Context
Students want posts to reach either the whole campus or only their group. Moderators need
to remove harmful content, group officers want to manage their own group, and authors need
a fair way to contest a decision. The rules must hold everywhere content leaves the server —
REST responses, WebSocket events and text sent to the LLM — otherwise group-only posts leak.

## Options considered

### Visibility levels
1. Campus-wide only — simplest, but groups cannot share internal announcements.
2. **Campus-wide or group-only per post** (chosen) — covers the customer request with two rules.
3. Fine-grained lists (named users, friends-of-friends) — expensive to check on every
   request and every live event, and not requested by any stakeholder.

### Who can moderate
1. Moderators only — consistent, but slow for large groups.
2. **Moderators anywhere + officers inside their own group** (chosen) — faster response,
   small blast radius if an officer account is misused.
3. Any group member can remove posts — easy to abuse (S5).

### Appeals
1. No appeals — no recourse for a wrongly hidden post; hurts S1's trust.
2. **One appeal, decided by a different moderator** (chosen) — second pair of eyes,
   cheap enough for pilot scale.
3. Committee/admin panel — too heavy for a pilot.

## Decision
- Every post has `visibility` = `campus` or `group`. A `group` post is visible only to
  members of its group (`GROUP_MEMBERSHIP`). Default is `campus`.
- All checks happen in one backend component (**Access Policy**, see
  `diagrams/c4-component.md`) called by the REST routers, the WebSocket hub before each
  broadcast, and the Summary service before building an LLM prompt. The frontend only hides
  buttons; it never decides access.
- Roles: `student` (default), `moderator`, `student_affairs` (global, on `USER.role`);
  `officer` (per group, on `GROUP_MEMBERSHIP.role`).
- Moderators can hide any post. Officers can remove posts in their own group only.
  Every hide/remove writes a `MODERATION_RECORD` in the same transaction as the post update.
- The author may appeal once. The appeal is assigned to a moderator other than the one who
  decided; the outcome (`restored` / `upheld`) is stored on the same record.
- Only `student_affairs` can verify a group (FR-9). Role grants are recorded in the audit log.

## Consequences
- **Positive:** One place to test authorization (NFR-7, NFR-10): a role × endpoint test
  matrix covers REST and WebSocket paths.
- **Positive:** The ER model carries the policy directly (`visibility`, membership role,
  appeal fields on `MODERATION_RECORD`), so the database can enforce part of it with constraints.
- **Negative:** Every live event must be filtered per recipient, which costs CPU on the hub;
  acceptable at pilot scale (NFR-2), revisit if broadcasts become slow.
- **Negative:** Appeals assume at least two active moderators (risk R6); fallback is review
  by Student Affairs.
- **Open:** How the first `student_affairs` account is created — planned as a seed/admin
  script, not an API endpoint (open question Q-2).
