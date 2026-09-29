# Project Scope

> Status: agreed by Omar, Salama, Makar (2026-09-29). Aro to review 1.4–1.5 against this.
> Salama leads 1.1–1.3 and owns further edits to this file.

## Product name
CampusConnect

## Problem
Students at MBZUAI don't have a single place to share campus-specific updates
(events, club posts, study groups, lost & found) — general social media is too broad and
noisy, and official channels (email, LMS announcements) are one-way and slow.

## First-release scope (Assignment 2 target)
- Student accounts, campus-verified (e.g. university email)
- Create/view text posts on a shared campus feed
- Comment on posts
- Basic visibility control (public to campus vs. specific groups/clubs)
- Moderation: campus moderators can hide/remove any post (report → hide → decision record, ADR-01);
  group officers can additionally remove posts within their own group
- AI feature: summarize long comment threads into a short digest (ADR-02, owner: Aro)

## Future features (out of scope for A1/A2, mentioned for context only)
- Real-time notifications (WebSockets)
- Rich text / media-heavy posts (React rich text editor)
- Direct messaging
- Events/calendar integration

## Explicitly excluded (this proof of concept, Assignment 1)
- No real authentication (mock/fictional users)
- No persistent database (in-memory only)
- No AI integration wired up (planned in architecture only)
- No production-grade styling/UX

## Open questions for the team
- Appeals process for moderation decisions (Salama/ADR-01)
- Aro to confirm this scope against 1.4–1.5 user stories and traceability matrix
