# Functional Requirements

> Lead: Salama (1.2). MoSCoW-prioritized, traced to user stories in `user-stories.md`.

## In scope (Assignment 2 release)

| ID | Requirement | Priority | Source | Story |
|---|---|---|---|---|
| FR-1 | A student can create a text post to a campus/group feed | Must | S1, S2 | US-1 |
| FR-2 | A student can view the campus feed, newest posts first | Must | S1 | US-2 |
| FR-3 | A student can comment on a post | Must | S1 | — |
| FR-4 | A post's audience can be set to campus-wide or a specific group | Must | S1, S2 | — (ADR-01) |
| FR-5 | A campus moderator can hide a reported post and record a decision | Must | S3 | US-3 (ADR-01) |
| FR-6 | A group officer can remove a post within their own group | Must | S2, S3 | US-4 (ADR-01) |
| FR-7 | A group officer can hand a draft post to another officer before publishing | Should | S2 | ADR-04 |
| FR-8 | The system generates a short summary of a long comment thread on request | Should | S1 | ADR-02 |
| FR-9 | A group can be marked "verified" by an authority (Student Affairs) | Should | S4 | — |
| FR-10 | A student can report a post for moderator review | Must | S1, S3 | US-3 |

## Explicitly out of scope (Won't — this project)

| ID | Excluded | Reason |
|---|---|---|
| EX-1 | Native mobile apps | Browser-only release; see scope.md |
| EX-2 | Direct messages | Not core to the campus-feed use case |
| EX-3 | Non-university/external users | University-only by design (FR-9 verification) |
| EX-4 | Payments | Out of scope for a social feed |
| EX-5 | Video hosting | Text/rich-text posts only (React rich text, A2) |
| EX-6 | Real (non-mocked) authentication in Assignment 1 POC | POC demonstrates the create-post flow only; see README |
