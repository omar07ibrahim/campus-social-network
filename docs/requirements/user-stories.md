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

## US-5: Comment on a post
As a student, I want to comment on a post, so that I can discuss it with others.

Acceptance criteria:
- Given a post exists, when I submit a comment (1–1000 chars), then it appears under the
  post, oldest first, without reloading the page.
- Given I submit an empty comment, when I hit submit, then I see a validation error and no
  comment is created (same validation shape as `POST /posts`, see `api-contract.md`).

## US-6: Set a post's audience
As a student or group officer, I want to choose whether a post is campus-wide or
group-only, so that I control who sees it.

Acceptance criteria:
- Given I am creating a post, when I pick "campus-wide" or "group-only", then the post is
  only visible to that audience when others view the feed.
- Given a post is group-only, when a student who isn't a member of that group views the
  campus feed, then the post does not appear.

## US-7: Student Affairs verifies a group
As a Student Affairs staff member, I want to mark a group as verified, so that students can
trust its official badge (S4, NFR-7).

Acceptance criteria:
- Given an unverified group, when Student Affairs marks it verified, then its posts show a
  "verified" badge in the feed.
- Given a group is not verified, when a student views its posts, then no verified badge is
  shown, and the group is visually distinguishable from verified ones.

## Assumptions
- "Group" membership and officer role are out of scope for the Assignment 1 POC (mocked/fictional).
- Moderation (US-3, US-4) and verification (US-7) are architecture-only for A1; not
  implemented in the POC backend.
- US-7's "Student Affairs staff member" role and its access control are not detailed further
  here — out of this assignment's depth, flagged for Assignment 2 auth design.

## Open questions
- Appeals process detail for US-3 (linked to ADR-01, still open).
- Exact reporting flow (who can report, is it rate-limited) — not yet specified.
- US-7: who grants Student Affairs staff their role in the system itself (bootstrapping
  problem) — not specified.

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
| US-5 Comment on post | FR-3 | NFR-1 | — | not in POC | Planned for A2 |
| US-6 Set post audience | FR-4 | — | ADR-01 | not in POC | Planned for A2 |
| US-7 Verify a group | FR-9 | NFR-7 | — | not in POC | Planned for A2 |

All FR/NFR now have at least one story or an explicit "unstoried" architecture-only row.
FR-9 still has no owning ADR (see `requirements-review.md` open questions) — Salama to
decide whether it needs its own ADR or folds into ADR-01's scope.
