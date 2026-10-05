# Product Scope

> Lead: Salama. Agreed by the whole team on 2026-09-29 (Step 1 of the brief), revised
> 2026-10-05 after the requirements review (see `requirements-review.md`, R-2).

## Product name
**CampusConnect** — a social network for the MBZUAI community.

## Problem
Students at MBZUAI have no single place to share campus-specific updates (events, club
posts, study groups, lost & found). General social media is too broad and noisy; official
channels (email, LMS announcements) are one-way and slow. Student groups prepare
announcements in chat apps and copy them by hand, so drafts get lost or overwritten, and
there is no shared, accountable way to deal with harmful posts.

## First release (built in Assignment 2)
- **Identity:** sign-in restricted to university email accounts (mocked SSO in development).
- **Communities:** students join groups; group officers manage their group; Student Affairs
  marks official groups as verified.
- **Publishing:** text posts with rich-text formatting (React editor) to the campus feed or a group.
- **Collaboration:** group officers co-edit and hand off draft announcements before
  publishing, with conflict detection (ADR-04).
- **Audience control:** each post is campus-wide or group-only (ADR-01).
- **Interaction:** comments on posts; feed and comments update live over WebSockets.
- **Moderation:** report → hide → recorded decision → one appeal to a second moderator (ADR-01).
- **AI feature:** on-request summary of long comment threads, with every summary point
  linked back to the comments it came from (ADR-02).

## Later releases (out of the first release, may come later)
- Events/calendar with RSVPs
- Image and file attachments
- Notifications by email or push
- Search across posts and groups
- Mobile apps

## Outside the product's scope
- Direct/private messaging
- Accounts for people outside the university
- Payments or marketplace features
- Video hosting

## Excluded from the Assignment 1 proof of concept
- No real authentication (author is a free-text name)
- No database (in-memory list, cleared on restart)
- No groups, comments, moderation, drafts, live updates or AI
- Plain HTML/JS instead of React; no production styling
