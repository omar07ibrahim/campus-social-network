# 1.4 User Stories and Scenarios

> Lead: Aro. Ten stories from four stakeholder groups, covering normal use, failures,
> exceptions and policy decisions. Each acceptance criterion is a Given/When/Then check.

| Story | Stakeholder | Part of the system | Covers |
|---|---|---|---|
| US-1 | Student (S1) | Identity, publishing | normal use, validation failure |
| US-2 | Student (S1) | Feed | normal use, empty case |
| US-3 | Moderator (S3) | Moderation | policy, duplicate report exception |
| US-4 | Group officer (S2) | Moderation | policy, permission failure |
| US-5 | Student (S1) | Interaction, live updates | normal use, failure, reconnect |
| US-6 | Student / officer (S1, S2) | Communities, audience control | policy, privacy |
| US-7 | Student Affairs (S4) | Communities | policy, permission failure |
| US-8 | Group officer (S2) | Real-time collaboration | concurrency exception, failure |
| US-9 | Student (S1) | AI feature | normal use, AI failure, output check |
| US-10 | Student (S1) + moderator (S3) | Moderation appeals | policy, exception |

## US-1: Sign in and create a post
As a **student**, I want to sign in with my university account and post an update, so that
the campus sees it and knows it comes from a real student.
- **Given** I sign in with an `@mbzuai.ac.ae` account, **when** sign-in completes, **then** I see the feed.
- **Given** I sign in with a non-university email, **when** sign-in completes, **then** I see
  "university accounts only" and no session is created.
- **Given** I am signed in, **when** I submit a post of 1–1000 characters, **then** it appears
  at the top of the feed without a page reload.
- **Given** I submit empty, whitespace-only or 1001+ character content, **when** I press Post,
  **then** I see a field error and no post is stored (contract: 422).

## US-2: View the campus feed
As a **student**, I want to see recent posts newest first, so that I stay informed.
- **Given** posts exist, **when** I open the feed, **then** they are ordered newest first, 20 per page.
- **Given** no posts exist, **when** I open the feed, **then** I see an empty feed and no error.

## US-3: Report and hide a harmful post
As a **campus moderator**, I want reported posts to reach me quickly and to hide them with
a reason, so that harmful content stops spreading but can still be reviewed.
- **Given** a student reports a post, **when** I have the moderation queue open, **then** the
  report appears within 2 seconds.
- **Given** the same student reports the same post again, **when** they submit, **then** they
  see "already reported" and no second report is stored.
- **Given** I hide a post with a reason, **when** anyone else loads the feed, **then** the post
  is gone, but its content, the reports and my decision are kept in a moderation record.

## US-4: Group officer removes a post in their group
As a **group officer**, I want to remove posts in my own group, so that I can keep it on topic.
- **Given** a post belongs to my group, **when** I remove it, **then** it disappears from the
  group feed and a moderation record names me as the decider.
- **Given** a post belongs to a group where I am not an officer, **when** I try to remove it,
  **then** I get "not allowed" (403) and the post is unchanged.

## US-5: Comment and see replies live
As a **student**, I want to comment on a post and see others' comments appear, so that I can
take part in the discussion.
- **Given** I can see a post, **when** I submit a 1–1000 character comment, **then** it appears
  under the post (oldest first) for me and, within 2 seconds, for others viewing the post.
- **Given** I submit an empty comment, **when** I press Send, **then** I see an error and nothing is stored.
- **Given** my connection drops and returns, **when** the page reconnects, **then** comments
  posted meanwhile are shown (refetched), with none missing or duplicated.

## US-6: Choose who sees my post
As a **student or group officer**, I want to post either campus-wide or to my group only,
so that internal group announcements stay inside the group.
- **Given** I am a member of group G, **when** I publish a group-only post to G, **then**
  members of G see it and non-members do not — in the feed, by direct link (404) and in live events.
- **Given** I am not a member of group G, **when** I try to post to G, **then** I get 403.
- **Given** I leave group G, **when** I reload the feed, **then** G's group-only posts are no longer shown.

## US-7: Student Affairs verifies a group
As a **Student Affairs staff member**, I want to mark official groups as verified, so that
students can trust who is posting.
- **Given** an unverified group, **when** I verify it, **then** its posts show a "verified"
  badge and an audit event records who verified it.
- **Given** a user without the Student Affairs role, **when** they call the verify action, **then** they get 403.

## US-8: Two officers prepare an announcement together
As a **group officer**, I want to edit a shared draft with my co-officers and hand it over,
so that we publish one agreed announcement without losing anyone's changes.
- **Given** two officers have draft version 7 open, **when** both save, **then** the first save
  creates version 8 and the second gets a conflict with the latest text to merge — no edit is lost.
- **Given** another officer opens the draft, **when** I am viewing it, **then** I see their
  name in the presence list within 2 seconds.
- **Given** the database fails while publishing, **when** I press Publish, **then** I see an
  error, no post is created, and the draft is unchanged so I can retry.

## US-9: Summarise a long thread and check it
As a **student**, I want a short summary of a long discussion that I can check against the
real comments, so that I can catch up without being misled.
- **Given** a thread with ≥ 20 comments I can see, **when** I click "Summarise", **then** I get
  3–6 points labelled "AI-generated", each linking to the comments it is based on.
- **Given** a thread with fewer than 20 comments, **when** I look at it, **then** the
  Summarise button is not offered.
- **Given** the AI service is unavailable, **when** I click "Summarise", **then** I see
  "summary unavailable, try later" within 10 seconds and the thread still works.
- **Given** I think a point is wrong, **when** I click "Flag", **then** the flag is stored for review.

## US-10: Appeal a moderation decision
As a **student whose post was hidden**, I want to appeal once, so that a mistake can be corrected.
- **Given** my post was hidden, **when** I submit an appeal, **then** it is assigned to a
  moderator other than the one who hid it.
- **Given** I already appealed this decision, **when** I try again, **then** I am told only one appeal is allowed.
- **Given** the moderator who hid my post tries to decide the appeal, **when** they submit,
  **then** the system refuses (403).
- **Given** the appeal is decided "restored", **when** students load the feed, **then** the post is visible again.
