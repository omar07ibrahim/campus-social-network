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
  requirements/      scope, stakeholders, user stories, traceability (Salama/Aro)
  architecture/       C4, sequence diagram, ER diagram, ADRs (Makar/Omar)
    adr/              4 architecture decision records, one per member
    diagrams/         editable diagram sources
  project-management/ responsibilities, workflow, risks, timeline (Aro)
```

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
