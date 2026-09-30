# Campus Social Network — Proof of Concept

MBZUAI campus social network, Assignment 1 (Requirements & Architecture) proof of concept.
Full product is built in Assignment 2 — this repo only demonstrates the "create a post" flow
end-to-end: browser form → FastAPI backend → validation → response → display.

## Team

| Member | Role |
|---|---|
| Salama | Requirements & product scope lead |
| Aro | Planning, validation & report lead |
| Makar | Backend & data architecture lead |
| Omar | Frontend & integration lead |

## Repo structure

```
backend/    FastAPI proof-of-concept API (in-memory, no DB)
frontend/   Plain HTML/JS browser form, no build step
docs/
  requirements/      scope, stakeholders, FR/NFR, user stories, traceability, review (Salama/Aro)
  architecture/       C4, sequence diagram, ER diagram, API contract, ADRs (Makar/Omar)
    adr/              4 architecture decision records, one per member
    diagrams/         editable diagram sources (Mermaid)
  project-management/ responsibilities, workflow, risks, timeline (Aro)
  demo-script.md       3-minute demo walkthrough (Omar)
```

See `docs/architecture/repository-structure.md` for the full breakdown (2.5) and the
Assignment 2 target layout.

## Document map (for the oral exam)

| Section | File |
|---|---|
| 1.1 Stakeholders & scope | `docs/requirements/stakeholders.md`, `scope.md` |
| 1.2 Functional requirements | `docs/requirements/functional-requirements.md` |
| 1.3 Non-functional requirements + driver ranking (2.1) | `docs/requirements/non-functional-requirements.md` |
| 1.4–1.5 User stories, traceability, review | `docs/requirements/user-stories.md`, `requirements-review.md` |
| 2.2–2.3 C4, sequence diagram | `docs/architecture/diagrams/` |
| 2.4 API contract | `docs/architecture/api-contract.md` |
| 2.5 Repository structure | `docs/architecture/repository-structure.md` |
| 2.6 ER diagram | `docs/architecture/diagrams/er-diagram.md` |
| 2.7 ADRs | `docs/architecture/adr/` |
| Section 3 Project management | `docs/project-management/README.md` |
| Demo | `docs/demo-script.md` |

## Running the proof of concept

### Backend
```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```
API docs at http://localhost:8000/docs

### Frontend
```bash
cd frontend
python3 -m http.server 5500
```
Open http://localhost:5500 in a browser. The form posts to `http://localhost:8000`.

## Proof-of-concept simplifications

- No real authentication — author name is free text
- No database — posts live in memory and reset on backend restart
- No AI integration — planned in the architecture, not implemented here
- CORS is wide open (`*`) for local demo purposes only

## Status

Early skeleton. Requirements, diagrams, and ADRs are drafts under `docs/` pending team review.
