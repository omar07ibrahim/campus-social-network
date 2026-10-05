# ADR-01: Audience Visibility and Access-Control Policy

- Status: draft (owner Salama — final wording still to review)
- Owner: Salama
- Date: 2026-10-05

## Context
Who can see a post, who can restrict its audience, and what visibility levels does the
platform need? Also covers: audience setting at post-creation (US-6/FR-4), group
verification badges (US-7/FR-9), and the appeals process for moderation decisions (US-3).

## Visibility levels
- **Campus-wide** — visible to every verified student (default).
- **Group-only** — visible only to members of the posting group (US-6).
- No "private"/DM-style visibility — explicitly out of scope (see `scope.md` exclusions).

## Alternatives considered — moderation authority
1. Moderators only (centralized, slower, consistent)
2. Moderators + group officers for their own group (chosen — faster response, some inconsistency risk)
3. Fully decentralized (any group member can remove) — rejected, too easy to abuse

## Alternatives considered — appeals process
1. No appeals (moderator decision is final) — rejected: no recourse for a wrongly hidden
   post, conflicts with S1's trust in the platform.
2. **Appeal to a second moderator, decision logged** (chosen) — the original author can
   request review; a different moderator (not the one who hid it) reviews the retained
   content + original decision record (`MODERATION_RECORD`, ADR-03) and either restores or
   upholds. Keeps a second set of eyes without needing a full committee process.
3. Committee/admin panel review — rejected for Assignment 2 scope, too heavy for pilot scale
   (NFR-2: 5,000 students).

## Decision
- Moderation authority: moderators + group officers for their own group.
- Appeals: author can request review; a second moderator (not the original) decides, using
  the retained content and decision record. The appeal outcome is itself recorded.
- Group verification (US-7/FR-9): a Student Affairs role (separate from "moderator") grants
  the verified badge; this ADR owns the policy, FR-9's exact UI/workflow is Assignment 2
  implementation detail, not a separate ADR (per `user-stories.md` traceability note).

## Consequences
- `MODERATION_RECORD` (ER diagram) needs an `appeal_status` and `appeal_decided_by` field,
  distinct from the original `moderator_id` — a schema detail Makar should carry into ADR-03's
  implementation, not just this ADR's text.
- Two-moderator appeal review assumes campus has ≥2 active moderators at any time — a
  staffing assumption, not a technical one; flagged here so project management (risks) can
  track it if it turns out false at pilot scale.
- Officers' power is scoped to their own group only — an officer cannot moderate another
  group's posts, limiting blast radius of a compromised/malicious officer account.
