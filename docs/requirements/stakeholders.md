# Stakeholder Analysis

> Lead: Salama (1.1). Drafted by the team 2026-09-29, informed by Omar's earlier individual
> CampusPulse lab exercise (different product, same course — reused as reference only, not
> as team history; see repo commit `29b5afc`).

Stakeholder types: end user, operations, business, regulator, negative stakeholder.

## S1 — Student
- Type: End user
- Goal: Discover and share campus updates in one place; comment and engage freely.
- Concern: Over-moderation/censorship of legitimate posts; loss of privacy.
- **Conflict:** wants maximum openness and speed of publishing — directly in tension with
  S3 (moderator) and S4 (administration), who want review and control before/after publishing.

## S2 — Group officer
- Type: End user (elevated — publishes on behalf of a verified group)
- Goal: Publish and hand off drafts quickly, reach the right audience (US-4, ADR-04).
- Concern: Approval friction or moderation delay makes the group look unresponsive.
- **Conflict:** wants fast, low-friction publishing — in tension with S3/S4's need for
  review before content reaches a wide audience.

## S3 — Campus moderator
- Type: Operations
- Goal: Act quickly on reports, retain evidence and a decision record for appeals (ADR-01).
- Concern: Losing evidence, untraceable decisions, unauthorised officer publishing.
- **Conflict:** wants control and an auditable process — in tension with S1/S2's desire for
  speed and minimal friction.

## S4 — University administration / Student Affairs
- Type: Business / regulator
- Goal: Platform stays compliant (official group verification, no impersonation), no PR
  incidents traceable to the university.
- Concern: Unverified groups, harmful content reaching students under the university's name.
- **Conflict:** wants verification/compliance overhead — in tension with S2's desire for fast
  onboarding of new groups, and with S1's expectation of open access.

## S5 — Bad actor / spammer (negative stakeholder)
- Type: Negative stakeholder
- Goal (adversarial): Post spam, impersonate a group, or repeatedly republish removed content.
- Concern (system's, not theirs): Must be mitigated by moderation (ADR-01) and account/group
  verification (S4), without over-restricting legitimate users (S1/S2).

## Cross-stakeholder conflict summary
| Tension | Sides | How the architecture addresses it |
|---|---|---|
| Speed vs. control | S1/S2 vs. S3/S4 | Publish-then-moderate (not pre-approval) — posts go live immediately, moderators act after a report (ADR-01) |
| Openness vs. compliance | S1 vs. S4 | Group verification badge (S4) without gating individual student posts |
| Officer autonomy vs. auditability | S2 vs. S3 | Draft hand-off is versioned (ADR-04); moderation decisions are recorded, not silent deletes (ADR-01) |
