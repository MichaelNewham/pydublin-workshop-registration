# PyCon Ireland 2026 - Event Registration System

A small web application for event registration, built with **Python + Flask
+ SQLAlchemy + SQLite**, plus Jinja2 templates, plain CSS, and vanilla JS.

Final project for **D4B - Elective 2: Business Programming** (**Option A** -
Event Registration Web App).

> **Live app:** https://pydublin-workshop-registration.onrender.com
> (Render free tier - first hit may take up to 50 s to cold-start, then fast.)

> See `Project - Business Programming May 2026 - Guidelines.pdf` for the
> official brief. This README explains how to **run locally**, how to
> **deploy**, and how the project is organised.

---

## What it does

A simple but complete event-registration tool for a small workshop:

- **Event information page** - date, location, description, price, seats remaining
- **Registration form** - name, email, phone, company, notes (with
  email-uniqueness + capacity checks enforced on the server)
- **List of participants** for the organiser, sorted newest-first
- **Detail page** per registration, with edit / cancel / restore actions
- **Two related database tables** - `Event` `<` `Registration` with a
  foreign key (1-to-many)
- **HTML / CSS styling** - custom stylesheet, responsive, accessible
- **One JavaScript interaction** - a live character counter on the notes
  field (`static/js/app.js`), so the user knows when they have hit the 280-
  character limit. Pure vanilla JS, no libraries.
- **Shared-password organiser gate** - the participants list and the
  edit/cancel/restore endpoints are gated behind a single shared password
  (`/login`) so attendee data is not publicly scrapable. The registration
  flow and the attendee's own detail page stay public.

## Tech stack

| Layer      | Tech                                                    |
|------------|---------------------------------------------------------|
| Language   | Python 3.11                                             |
| Framework  | Flask 3 (`flask`)                                       |
| ORM        | SQLAlchemy (`flask_sqlalchemy`)                         |
| Database   | SQLite (file-based; ephemeral on Render, by design)     |
| Templates  | Jinja2 (ships with Flask)                               |
| Styling    | Plain CSS in `static/css/styles.css`                    |
| JS         | Vanilla JS in `static/js/app.js` (no libraries)         |
| Server     | Gunicorn (production WSGI; Render runs this)            |
| Deploy     | Render via `render.yaml` (push-to-deploy)               |
| CI         | GitHub Actions (`.github/workflows/ci.yml`)             |

> **CI note:** the workflow file lives in the repo but needs a one-time
> permission grant to start running. See [`docs/CI_SETUP.md`](docs/CI_SETUP.md).

---

## Repository layout

```
Project/
|- README.md                       <- you are here
|- AUTHORS.md                      <- the four students + IDs
|- requirements.txt                <- pip dependencies
|- run.py                          <- dev entry point (python run.py)
|- render.yaml                     <- Render push-to-deploy config
|- Procfile                        <- alt deploy hint (web: gunicorn run:app)
|- .env.example                    <- env-var template (copy to .env)
|- .github/workflows/ci.yml        <- lint + boot-test on every push/PR
|
|- event_registration/             <- the Flask app (Python package)
|  |- __init__.py                  <- create_app() factory + auto-seed
|  |- config.py                    <- Config class (reads env vars)
|  |- extensions.py                <- `db = SQLAlchemy()`
|  |- models.py                    <- Event + Registration models (Block A)
|  |- routes.py                    <- all HTTP routes + validation (Block A)
|  |- seed.py                      <- idempotent seed on first boot
|  |- templates/                   <- HTML (Block B)
|  |  |- base.html                 <- shared layout (header / footer / CSS / JS)
|  |  |- home.html, register.html
|  |  |- participants.html, detail.html, edit.html, error.html
|  |- static/
|     |- css/styles.css            <- all styling (Block C)
|     |- js/app.js                 <- the JavaScript interaction - char counter (Block C)
|
|- data/seed_events.csv            <- matches the seed_demo_data() in code
|- docs/                           <- report, video script, contribution csv
   |- Short_Report.md
   |- Video_Demo_script.md
   |- Individual_Contribution.csv
   |- AI_USE_STATEMENT.md
```

---

## How to run

### Local development

```bash
# 1. Clone + enter the repo
git clone https://github.com/MichaelNewham/pydublin-workshop-registration
cd pydublin-workshop-registration

# 2. (Optional but recommended) virtualenv
python -m venv .venv && source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the dev server
python run.py
# -> open http://localhost:5000
```

On first boot the schema is created and a demo Event + two sample
registrations are seeded automatically (`seed.py`), so the home and
participants pages are non-empty without any setup.

### Production / live deploy (Render - free tier)

This repo has a `render.yaml`, so deployment is push-to-deploy:

1. Go to https://render.com and sign in with GitHub (one-time).
2. **New -> Blueprint** -> pick this repo.
3. Render reads `render.yaml`, installs deps, runs `gunicorn run:app`.
4. You get a stable public URL like
   `https://pydublin-workshop-registration.onrender.com`.
5. **Every `git push` to `main` triggers an auto-redeploy** - so the tutor
   always sees the latest code.

**The current live deployment**: https://pydublin-workshop-registration.onrender.com
(auto-synced from `main`; see the Render dashboard for deploy history).

SQLite on Render is ephemeral - the DB resets on each deploy. That's
intentional for a marking demo (the seed runs fresh each time). For a
production build, swap `DATABASE_URL` to a Render Postgres instance.

---

## Decisions and assumptions

| Decision           | Value                                                |
|--------------------|------------------------------------------------------|
| Option             | A - Event Registration Web App                       |
| Stack              | Flask + SQLAlchemy + SQLite + Jinja2 + plain CSS/JS  |
| Event type         | Workshop                                             |
| Event name         | PyCon Ireland 2026 - Python for Business         |
| Registration fields| name, email, phone, company, notes                   |
| Organiser gate      | Shared password at `/login` (env: `ORGANISER_PASSWORD`)   |
| Git remote         | `MichaelNewham/pydublin-workshop-registration` (private; invite-only for collaborators) |

---

## Development workflow (small team, 4 people)

The project is split into four functional blocks that together cover the
entire repo. The split mirrors the `Group_Evaluation.pdf` role template
(database/backend 30%, interface/design 25%, testing/docs 25%,
integration/PM 20%):

| Block | Owner            | Role                | Owns                                                          | %   |
|-------|------------------|---------------------|---------------------------------------------------------------|-----|
| **A** | Michael Newham   | Backend & Data      | `models.py`, `routes.py`, `seed.py`, `config.py` (ORM + CRUD + validation) | 30% |
| **B** | Sergiu D         | Templates (Views)   | All `templates/*.html` + the form/list/detail/edit UIs        | 25% |
| **C** | Paul Sealy       | CSS + JavaScript    | `static/css/styles.css` + `static/js/app.js` (incl. the JS interaction + responsiveness) | 25% |
| **D** | Alessandro Genco | Docs, Testing & PM  | `README.md`, `docs/`, `render.yaml`, CI workflow, demo video, final QA | 20% |

### Build order

1. **A (Michael)** lands the models + routes first - every other block calls into the URL routes.
2. **B (Sergiu)** builds the five Jinja templates on top of A's routes, wiring up the forms and navigation.
3. **C (Paul)** can start in parallel with B - the CSS classes are decoupled from the markup. Adds the JS interaction in `static/js/app.js`.
4. **D (Alessandro)** drafts `docs/` alongside A/B/C; writes the test log as features land; records the demo video and does final QA last.

A is the only hard prerequisite (B's templates need A's routes). C is fully
parallel. See `docs/Individual_Contribution.csv` for the canonical split.

> **New to the project?** The per-student setup guide + tasks per block is in
> [`docs/COLLABORATOR_NOTES.md`](docs/COLLABORATOR_NOTES.md).

---

## Mapping to course requirements (Option A deliverables)

| Requirement (from the Guidelines PDF)  | Where in this repo                                  |
|----------------------------------------|-----------------------------------------------------|
| Event information page                 | `routes.home` -> `templates/home.html`              |
| Registration form                      | `routes.register` -> `templates/register.html`      |
| Database to store registrations        | `models.py` (SQLAlchemy, `Event` + `Registration`)  |
| List of registered participants        | `routes.participants` -> `templates/participants.html` |
| Detail page for each registration      | `routes.detail` -> `templates/detail.html`          |
| Edit or cancel a registration          | `routes.edit` / `routes.cancel` / `routes.restore`  |
| Basic HTML/CSS styling                 | `templates/base.html` + `static/css/styles.css`     |
| At least one simple JavaScript interaction | `static/js/app.js` (live character counter) |
| Two related tables                     | `Registration.event_id` -> `Event.id` (FK)          |
| README                                 | this file                                           |
| AI-use statement                       | `docs/AI_USE_STATEMENT.md` (linked from the report) |
| Short report                           | `docs/Short_Report.md`                              |
| Demo video script                      | `docs/Video_Demo_script.md`                         |
| Individual contribution                | `docs/Individual_Contribution.csv`                  |

---

## Routes reference

| Method | Path                              | Purpose                          |
|--------|-----------------------------------|----------------------------------|
| GET    | `/`                               | Event information page           |
| GET    | `/register`                       | Show the registration form       |
| POST   | `/register`                       | Create a registration            |
| GET    | `/participants`                   | List all active registrations    |
| GET    | `/registration/<id>`              | Detail page for one registration |
| GET    | `/registration/<id>/edit`         | Show the edit form               |
| POST   | `/registration/<id>/edit`         | Save edits                       |
| POST   | `/registration/<id>/cancel`       | Cancel (soft-delete)             |
| POST   | `/registration/<id>/restore`      | Restore a cancelled one          |
