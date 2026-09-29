# User Stories & Acceptance Criteria — DRAFT (lead: Aro)

> Status: template only, not yet written. Based on agreed scope in `scope.md`.
> Aro leads 1.4–1.5: at least 4 stories, acceptance criteria, review, assumptions, open questions.

## Story template
```
As a <role>, I want <goal>, so that <benefit>.

Acceptance criteria:
- Given <context>, when <action>, then <outcome>
- ...
```

## Candidate stories (from agreed scope — flesh out or replace)
1. As a student, I want to post an update to the campus feed, so that others can see it.
   (maps to POST /posts — see api-contract.md)
2. As a student, I want to see recent campus posts, so that I stay informed.
   (maps to GET /posts)
3. As a campus moderator, I want to hide a reported post, so that harmful content stops spreading.
4. As a group officer, I want to remove a post in my own group, so that I can moderate my community.

## Traceability matrix
| Story | Requirement | ADR | POC demo | Status |
|---|---|---|---|---|
| 1 | Create post | — | backend/frontend | POC done |
| 2 | View feed | — | backend/frontend | POC done |
| 3 | Moderator removes post | ADR-01 | not in POC | planned A2 |
| 4 | Officer removes group post | ADR-01 | not in POC | planned A2 |

## Assumptions & open questions
_(Aro to fill in.)_
