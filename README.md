# CampusConnect — Campus Social Network

AI1220 Assignment 1 (Requirements Engineering, Architecture & Proof of Concept), MBZUAI.
The full product is built in Assignment 2. This repository contains the report, the
editable diagram sources and a proof of concept of one interaction: **creating a campus post**
(browser form → FastAPI backend → validation → response → display).

**The submitted report is [`Report.pdf`](Report.pdf).**

## Team

| Member | GitHub | Lead role |
|---|---|---|
| Salama Aldhaheri | @SalamaAldhaheri | Requirements & product scope (1.1–1.3, 2.1, ADR-01) |
| Aro Dana | @arokurd | Planning, validation & report (1.4–1.5, Section 3, ADR-02, report assembly) |
| Makar Ulesov | @triplepiner | Backend & data architecture (POC backend, 2.4–2.6, component diagram, ADR-03) |
| Omar Ibrahim | @omar07ibrahim | Frontend & integration (POC frontend, 2.2–2.3, README, demo, ADR-04) |

## Running the proof of concept

Requires Python 3.10+.

### Backend (terminal 1)
```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --port 8000
```
Interactive API docs: http://localhost:8000/docs

### Frontend (terminal 2)
```bash
cd frontend
python3 -m http.server 5500
```
Open http://localhost:5500. The page calls the backend at `http://localhost:8000`.

### Tests
```bash
cd backend && source .venv/bin/activate && pytest -q     # 8 passed
```

## Proof-of-concept simplifications
Full table with reasons: [`docs/poc.md`](docs/poc.md).
- No authentication — `author` is free text (A2: university sign-in, roles).
- No database — posts live in memory and disappear when the backend restarts (A2: PostgreSQL, ADR-03).
- Plain HTML/JS instead of React with rich text.
- No groups, visibility, comments, moderation, drafts, live updates or AI summaries.
- CORS allows any origin, for the local two-port demo only.

## Where each report section lives

| Section | File |
|---|---|
| Product scope | `docs/requirements/scope.md` |
| 1.1 Stakeholders | `docs/requirements/stakeholders.md` |
| 1.2 Functional requirements | `docs/requirements/functional-requirements.md` |
| 1.3 Non-functional requirements, 2.1 drivers | `docs/requirements/non-functional-requirements.md` |
| 1.4 User stories | `docs/requirements/user-stories.md` |
| 1.5 Validation & traceability | `docs/requirements/requirements-review.md` |
| 2.2 C4 context / container / component | `docs/architecture/diagrams/c4-*.md` |
| 2.3 Behaviour & design decisions | `docs/architecture/behaviour-and-design.md` |
| 2.3 Collaborative sequence diagram | `docs/architecture/diagrams/sequence-draft-handoff.md` |
| 2.4 Interfaces | `docs/architecture/api-contract.md` |
| 2.5 Repository structure | `docs/architecture/repository-structure.md` |
| 2.6 Data model | `docs/architecture/diagrams/er-diagram.md` |
| 2.7 ADRs | `docs/architecture/adr/` |
| 3 Project management | `docs/project-management/README.md` |
| 4 Proof of concept | `docs/poc.md`, `docs/architecture/diagrams/sequence-create-post.md`, `docs/demo-script.md` |

Diagrams are Mermaid source inside these Markdown files (editable as text, rendered by
GitHub and in the PDF).

## Rebuilding Report.pdf
```bash
python3 -m venv .venv-report && source .venv-report/bin/activate
pip install -r docs/report-requirements.txt && playwright install chromium
python docs/build_report.py
```
