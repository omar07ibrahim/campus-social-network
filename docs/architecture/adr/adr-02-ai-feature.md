# ADR-02: AI Feature, Data Used, and How Users Check Its Output

- **Status:** Accepted
- **Owner:** Aro
- **Date:** 2026-10-05 (topic agreed 2026-09-29)
- **Feasibility review:** Makar (adapter + mock in FastAPI, citation check), Omar (summary
  panel with links to comments) — both feasible in Assignment 2.
- **Related:** FR-8, FR-15, NFR-10, NFR-12, US-9, A-5, A-6

## Context
Assignment 2 requires an LLM integration that meets a real community need. Popular posts
(events, course questions, housing) collect dozens of comments; students who arrive late
must scroll through everything or miss the outcome. An LLM can be wrong, so its output must
be checkable, and it must not become a way to read content the user is not allowed to see
(ADR-01) or to send unnecessary personal data to a third party (NFR-10).

## Options considered
1. **Thread summarisation on request, with citations** — clear need for S1; summarising
   visible text is low-risk; each point can be checked against the comments it cites.
2. **Automatic toxicity flagging for moderators** — useful to S3, but false positives
   directly affect what students may say and it overlaps with human moderation policy
   (ADR-01); errors are harder for users to check.
3. **AI drafting of announcements for officers** — helpful, but generated text is published
   under a group's name; verifying it is the officer's job, not the system's.
4. **No AI feature** — not allowed by the brief.

For option 1 we also considered **automatic summaries on every thread** (rejected: cost and
unrequested AI text everywhere) versus **on request** (chosen).

## Decision
Option 1, on request.
- **Trigger:** a "Summarise" button on threads with ≥ 20 visible comments (FR-8).
- **Data sent:** for each comment the requester can see — comment id, author display name,
  text. No emails, user ids, group membership, other threads, or hidden/removed comments.
  The Access Policy selects the comments before the prompt is built.
- **Model:** called through an `LLMAdapter` interface. A deterministic `MockSummarizer` is
  used in development and tests; the real provider is set by configuration (A-5), with the
  key kept on the server only.
- **Output format:** 3–6 points, each with `source_comment_ids`. The Summary service drops
  any point with no citations or with ids not in the input.
- **How users check it:** the panel is labelled "AI-generated — check the linked comments";
  clicking a point highlights its source comments; "Flag as wrong" stores a flag (FR-15).
- **Stored:** the summary, the comment count at generation time and flag count
  (`THREAD_SUMMARY`), so it can be reviewed and regenerated once 10+ new comments arrive.
- **Failure:** 8 s timeout, one retry, then "summary unavailable"; the thread works normally.

## Consequences
- **Positive:** The feature addresses a clear S1 need and its errors are visible and
  correctable by the user, not hidden.
- **Positive:** Citations give the team a measurable quality check in Assignment 2: share of
  points whose cited comments actually support them, plus flag rate.
- **Positive:** The adapter + mock means tests and the demo need no paid API calls.
- **Negative:** Citations do not prove a point is a fair summary — a point can cite real
  comments but still misstate them; flags and spot checks are the mitigation.
- **Negative:** Comment text leaves our system for the provider (assumption A-6); a
  self-hosted model can replace it behind the same adapter if the university requires.
- **Negative:** Summaries can go stale as the thread grows; the UI shows the comment count
  they were based on.
