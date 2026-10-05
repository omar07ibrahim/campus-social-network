# 2.2 C4 — Level 1: System Context

> Lead: Omar. Editable Mermaid source; renders on GitHub and in `Report.pdf`.

```mermaid
C4Context
    title CampusConnect — System Context

    Person(student, "Student", "Reads and writes posts, comments, joins groups, asks for thread summaries")
    Person(officer, "Group officer", "Prepares drafts with other officers, publishes for the group")
    Person(moderator, "Campus moderator", "Handles reports, hides posts, decides appeals")
    Person(affairs, "Student Affairs", "Verifies official groups, grants moderator role")

    System(campusconnect, "CampusConnect", "Campus social network: feed, groups, drafts, moderation, AI thread summaries")

    System_Ext(idp, "University sign-in", "Identity provider (OIDC). Mocked in development")
    System_Ext(llm, "LLM Provider", "Summarises comment threads. Mock in development and tests")

    Rel(student, campusconnect, "Uses", "HTTPS + WebSocket")
    Rel(officer, campusconnect, "Co-edits drafts, publishes", "HTTPS + WebSocket")
    Rel(moderator, campusconnect, "Moderates", "HTTPS + WebSocket")
    Rel(affairs, campusconnect, "Verifies groups", "HTTPS")
    Rel(campusconnect, idp, "Verifies university identity", "OIDC")
    Rel(campusconnect, llm, "Sends visible comments, gets cited summary", "HTTPS/JSON")
```

## Explanation
- **System boundary:** CampusConnect is the only system we build. Everything inside it is
  shown in the container diagram.
- **Users:** the four human stakeholder groups from `stakeholders.md` (S1–S4). The bad
  actor (S5) is not drawn as a user; the design defends against them through identity
  (FR-11) and authorization (ADR-01).
- **External systems:** the university identity provider, so only university accounts can
  sign in (FR-11), and an LLM provider for thread summaries (FR-8). Both sit behind backend
  adapters, so mocks replace them in development and in the POC — no paid calls needed.
- **Communication:** browsers use HTTPS for requests and a WebSocket for live updates; only
  the backend talks to the external systems, so no secret reaches the browser.
