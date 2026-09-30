# User Stories & Acceptance Criteria

> Lead: Aro. Drafted together by the team (2026-09-29) from the agreed scope; Aro to refine
> wording, add assumptions/open questions, and own the traceability matrix going forward.

## US-1: Create a post
As a student, I want to post an update to the campus feed, so that others can see it.

Acceptance criteria:
- Given I am on the campus feed, when I submit a post with an author name and content
  (1–1000 chars), then the post appears at the top of the feed within the same page load.
- Given I submit a post with empty content, when I hit submit, then I see a validation
  error and no post is created (matches `POST /posts` 422 response).

## US-2: View the campus feed
As a student, I want to see recent campus posts, so that I stay informed.

Acceptance criteria:
- Given posts exist, when I open the feed, then I see them ordered newest first.
- Given no posts exist, when I open the feed, then I see an empty feed (no error).

## US-3: Moderator hides a reported post
As a campus moderator, I want to hide a reported post, so that harmful content stops spreading.

Acceptance criteria:
- Given a post has been reported, when a moderator hides it, then it disappears from the
  public feed but the content, reporter, and decision are retained for appeal review.
- Given a post is hidden, when a non-moderator views the feed, then the post is not shown.

## US-4: Group officer moderates their own group
As a group officer, I want to remove a post in my own group, so that I can moderate my community.

Acceptance criteria:
- Given a post belongs to my group, when I remove it, then it disappears from that group's feed.
- Given a post belongs to a group I don't officer, when I try to remove it, then I am denied.

## Assumptions
- "Group" membership and officer role are out of scope for the Assignment 1 POC (mocked/fictional).
- Moderation (US-3, US-4) is architecture-only for A1; not implemented in the POC backend.

## Open questions
- Appeals process detail for US-3 (linked to ADR-01, still open).
- Exact reporting flow (who can report, is it rate-limited) — not yet specified.

## Traceability matrix

Full requirement definitions: `functional-requirements.md`, `non-functional-requirements.md`.
Stakeholder sources: `stakeholders.md`.

| Story | Functional req. | NFR | ADR | POC demo / test | Status |
|---|---|---|---|---|---|
| US-1 Create post | FR-1 | NFR-1 | — | `POST /posts`, frontend form, `test_create_post` | Implemented in POC |
| US-2 View feed | FR-2 | NFR-1 | — | `GET /posts`, frontend list, `test_list_posts_newest_first` | Implemented in POC |
| US-3 Moderator hides post | FR-5, FR-10 | NFR-4, NFR-5 | ADR-01 | not in POC | Planned for A2 |
| US-4 Officer moderates group | FR-6 | NFR-5 | ADR-01 | not in POC | Planned for A2 |
| (unstoried) Draft hand-off | FR-7 | NFR-8 | ADR-04 | not in POC | Planned for A2 |
| (unstoried) Thread summary | FR-8 | — | ADR-02 | not in POC | Planned for A2 |
| (unstoried) Data persistence | — | NFR-2, NFR-5, NFR-7 | ADR-03 | not in POC | Planned for A2 |

**Gaps flagged by this matrix:** FR-3 (comment), FR-4 (audience setting), and FR-9 (group
verification) have no user story yet — Aro to add before the final report, or explicitly
mark as backlog for Assignment 2 if not user-facing enough to need one.
