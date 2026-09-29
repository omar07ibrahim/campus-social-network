# Project Scope — DRAFT (for team review, lead: Salama)

> Status: draft proposal, not yet agreed. Salama leads 1.1–1.3 and should edit/replace this directly.

## Product name
CampusConnect (placeholder — rename if the team prefers)

## Problem
Students at [university name] don't have a single place to share campus-specific updates
(events, club posts, study groups, lost & found) — general social media is too broad and
noisy, and official channels (email, LMS announcements) are one-way and slow.

## First-release scope (Assignment 2 target)
- Student accounts, campus-verified (e.g. university email)
- Create/view text posts on a shared campus feed
- Comment on posts
- Basic visibility control (public to campus vs. specific groups/clubs)
- Basic moderation (report a post, admin remove)
- One AI feature (e.g. auto-summarizing long threads, or flagging spam) — owner: Aro (ADR)

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
- Confirm university/campus context (real or fictional?)
- Confirm the one AI feature to commit to for the ADR
- Confirm moderation policy: who can remove a post, appeals?
