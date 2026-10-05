# 1.2 Functional Requirements

> Lead: Salama. MoSCoW priority for the Assignment 2 release. Every requirement states what
> the user does and how the system observably responds, so it can be tested. Stakeholder IDs
> (S1–S5) are from `stakeholders.md`; story IDs (US-x) from `user-stories.md`.

## Requirements by area

| ID | Area | The user… | The system responds by… | Priority | Source | Story |
|---|---|---|---|---|---|---|
| FR-11 | Identity | signs in with a university email account | creating a session only for addresses on the university domain; any other address gets an error and no session | Must | S4, S5 | US-1 |
| FR-12 | Communities | joins or leaves a group; a group's creator appoints officers | updating membership immediately; only members see the group's group-only posts | Must | S1, S2 | US-6 |
| FR-9 | Communities | (Student Affairs) marks a group as verified | showing a "verified" badge on all of that group's posts | Should | S4 | US-7 |
| FR-1 | Publishing | creates a post (1–1000 characters, rich text) | storing it and returning it with an id and timestamp; empty or too-long content is rejected with a field-level error and nothing is stored | Must | S1, S2 | US-1 |
| FR-2 | Publishing | opens the campus feed | listing visible posts newest first; an empty feed shows no error | Must | S1 | US-2 |
| FR-7 | Real-time collaboration | (officer) edits a shared group draft and hands it to another officer | saving each edit with a version number; a save based on an outdated version is rejected and the officer is shown the latest text to merge; other officers viewing the draft see who is editing | Should | S2 | US-8 |
| FR-13 | Real-time collaboration | has the feed or a post's comments open | delivering new posts/comments they are allowed to see without a page reload | Must | S1, S2 | US-5 |
| FR-4 | Audience control | chooses campus-wide or group-only when publishing | returning a group-only post only to members of that group, in every endpoint and live event | Must | S1, S2 | US-6 |
| FR-3 | Interaction | comments on a post they can see (1–1000 characters) | adding the comment under the post, oldest first; empty comments are rejected | Must | S1 | US-5 |
| FR-10 | Moderation | reports a post with a reason | queuing the report for moderators; the same user cannot report the same post twice | Must | S1, S3 | US-3 |
| FR-5 | Moderation | (moderator) hides a reported post with a reason | removing it from all feeds while keeping the content, report and decision in a moderation record | Must | S3 | US-3 |
| FR-6 | Moderation | (officer) removes a post in their own group | removing it and recording the decision; the same action on another group's post is denied | Must | S2, S3 | US-4 |
| FR-14 | Moderation | (author of a hidden post) appeals once | assigning the appeal to a moderator other than the one who hid it; the outcome (restore/uphold) is recorded and shown to the author | Should | S1, S3 | US-10 |
| FR-8 | AI feature | requests a summary of a thread with at least 20 comments | returning a short summary built only from comments the requester can see, labelled as AI-generated | Should | S1 | US-9 |
| FR-15 | AI feature | clicks a summary point, or flags a summary as wrong | showing the source comments behind that point; a flagged summary is logged for review and can be regenerated | Should | S1, S4 | US-9 |

## The AI feature in brief (details in ADR-02)
- **Whose need:** students (S1) who open a long discussion and cannot read 50+ comments.
- **Data used:** the text of the visible comments in that thread and the authors' display
  names, nothing else — no email addresses, no other threads, no group-only content the
  requester cannot already see.
- **How the output is checked:** every summary point cites the comment ids it came from
  (FR-15); users can open the cited comments and flag a wrong summary; flagged summaries
  are reviewed by the team during Assignment 2 to measure accuracy.

## Required behaviour vs. design choices
The table above is **required behaviour**. These are **design choices** recorded elsewhere,
and could change without changing the requirements:
- Optimistic concurrency with version numbers for drafts (ADR-04).
- PostgreSQL as the data store (ADR-03).
- Second-moderator appeal review (ADR-01).
- Summaries generated on request rather than automatically (ADR-02).

## Technology constraints (given by the course, not chosen by us)
- Backend: Python with FastAPI; live updates over WebSockets.
- Frontend: React with a rich-text editor.
- An LLM integration; paid API calls are not required, so a mock provider must be possible.

## Won't (outside the product)
| ID | Excluded | Reason |
|---|---|---|
| EX-1 | Native mobile apps | Browser-only release |
| EX-2 | Direct messages | Not core to a campus feed; raises privacy and moderation load |
| EX-3 | Non-university users | University-only by design (FR-11) |
| EX-4 | Payments | Not a social-feed need |
| EX-5 | Video hosting | Storage and moderation cost out of proportion to a pilot |
| EX-6 | Real authentication in the Assignment 1 POC | POC demonstrates only the create-post flow; see README |
