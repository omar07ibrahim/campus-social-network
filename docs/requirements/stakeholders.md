# 1.1 Stakeholder Analysis

> Lead: Salama. Drafted by the team 2026-09-29, influence added 2026-10-05.

Five stakeholder groups: four that the product serves or answers to, and one negative
stakeholder the design must defend against. "Influence" describes how strongly each group
shapes requirements and how that shows up in the system.

## S1 — Student
- **Type:** End user (largest group).
- **Goals:** Discover and share campus updates in one place; comment and engage freely;
  catch up on long discussions quickly.
- **Concerns:** Over-moderation of legitimate posts; group-only posts leaking to outsiders;
  personal data being sent to an AI service.
- **Influence:** High on usability and performance — adoption depends on them (NFR-1, NFR-11).
  Low on policy: they cannot change moderation rules, but can appeal decisions (FR-14).

## S2 — Group officer
- **Type:** End user with elevated rights within one group.
- **Goals:** Prepare announcements together with other officers, hand drafts off, publish
  quickly to the right audience (FR-7, ADR-04).
- **Concerns:** Losing a co-officer's edits; moderation delay making the group look unresponsive.
- **Influence:** Medium — drives the collaboration and audience-control requirements; can
  remove posts only in their own group (FR-6).

## S3 — Campus moderator
- **Type:** Operations (staff or trained student volunteers).
- **Goals:** Act quickly on reports; keep evidence and a decision record for appeals (ADR-01).
- **Concerns:** Losing evidence; untraceable decisions; abuse of officer powers.
- **Influence:** High on moderation, audit and data-integrity requirements (NFR-4, NFR-5,
  NFR-12), which in turn drove the PostgreSQL decision (ADR-03).

## S4 — University administration / Student Affairs
- **Type:** Business owner and internal regulator.
- **Goals:** Platform stays compliant with university policy; official groups are
  verified; no incident under the university's name; student data handled lawfully.
- **Concerns:** Impersonated groups; harmful content; privacy breaches; AI misuse of student data.
- **Influence:** Very high — can shut the platform down. Sets identity (FR-11),
  verification (FR-9), privacy (NFR-10) and AI data rules (ADR-02).

## S5 — Bad actor / spammer (negative stakeholder)
- **Type:** Negative stakeholder.
- **Goal (adversarial):** Post spam, impersonate a group, republish removed content, or
  extract group-only content.
- **Influence:** Indirect but real — the reason for verified sign-in, rate limits, server-side
  authorization checks and the audit log (FR-11, NFR-7, NFR-12).

## Where interests conflict
| Tension | Sides | How the requirements/architecture resolve it |
|---|---|---|
| Speed vs. control | S1/S2 vs. S3/S4 | Publish-then-moderate, not pre-approval: posts go live immediately and moderators act on reports within the NFR-4 target (ADR-01) |
| Openness vs. compliance | S1 vs. S4 | Verification badge for groups (FR-9) instead of gating individual student posts |
| Officer autonomy vs. auditability | S2 vs. S3 | Officers may remove posts in their own group only; every removal produces a moderation record (FR-6, NFR-5) |
| Moderator authority vs. fairness to authors | S3 vs. S1 | One appeal, decided by a different moderator (FR-14, ADR-01) |
| AI convenience vs. privacy | S1 vs. S1/S4 | Summaries only use comments the requester can already see; nothing is stored by the provider (ADR-02, NFR-10) |
