# PyCon Ireland 2026 — Event Registration System

> **Course:** D4B — Elective 2: Business Programming (Option A — Event Registration Web App)
> **Team:** Michael Newham · Sergiu D · Paul Sealy · Alessandro Genco

> **🔴 Live app (click to try it):** https://pydublin-workshop-registration.onrender.com
> **📦 Source code:** https://github.com/MichaelNewham/pydublin-workshop-registration
> **🟢 CI status:** [![CI](https://github.com/MichaelNewham/pydublin-workshop-registration/actions/workflows/ci.yml/badge.svg)](https://github.com/MichaelNewham/pydublin-workshop-registration/actions)

A small web application for event registration, built with **Python + Flask
+ SQLAlchemy** and a SQLite (dev) / Postgres (prod) database, plus Jinja2
templates, plain CSS, and one vanilla-JS interaction.

> ⏱️ The live app is on Render's free tier. The first request after an
> idle period may take ~30–50 s to cold-start; subsequent requests are fast.

---

## Try the live app (30-second walkthrough)

You don't need to clone anything — just click through the live deployment.

1. **Home / event information page** — https://pydublin-workshop-registration.onrender.com/
   *(Shows the event title, date, location, price, live "seats remaining"
   count, and the day-of schedule.)*
2. **Registration form (public)** — https://pydublin-workshop-registration.onrender.com/register
   *(Type a note → watch the live character counter turn red past 280 chars.
   That's the JavaScript interaction.)*
3. **Submit** → you'll be redirected to your own confirmation page at
   `/registration/<id>`. Try the **same email again** → server blocks it.
4. **Organiser area (gated)** — https://pydublin-workshop-registration.onrender.com/login
   Password (demo only): **`pydublin-2026`**
   → Shows the Participants list, lets you **Edit**, **Cancel**, and **Restore**.
5. Without the password, `/participants` correctly redirects to `/login`
   (attendee data is **not** publicly scrapable).

---

## What it does

| Feature                                         | Where (Flask)                                       |
|-------------------------------------------------|-----------------------------------------------------|
| Event information page                          | `GET /` → `templates/home.html`                     |
| Registration form with server-side validation   | `GET /POST /register` → `templates/register.html`   |
| List of participants (organiser)                | `GET /participants` → `templates/participants.html` |
| Detail page per registration                    | `GET /registration/<id>` → `templates/detail.html`  |
| Edit / Cancel / Restore (soft-delete audit)     | `/registration/<id>/{edit,cancel,restore}`          |
| Two related tables (`Event` 1 — N `Registration`) | `event_registration/models.py` (SQLAlchemy FK)    |
| Server-side capacity + duplicate-email checks   | `register()` in `event_registration/routes.py`      |
| Shared-password organiser gate (`/login`)       | `event_registration/auth.py` + `@login_required`    |
| Basic HTML / CSS styling (responsive, accessible) | `templates/base.html` + `static/css/styles.css`     |
| JavaScript interaction — live char counter | `static/js/app.js` (vanilla, no libraries)          |

Capacity is enforced in `routes.py:register()`: a `MAX_CAPACITY` query on
`Event` blocks overbooking. Duplicate emails are blocked with a server-side
"You're already registered" message. Cancellation is a soft-delete
(`status = 'cancelled'`) so the audit trail is preserved and the seat is
freed.

---

## Tech stack

| Layer     | Tech                                                |
|-----------|-----------------------------------------------------|
| Language  | Python 3.11                                         |
| Framework | Flask 3                                             |
| ORM       | SQLAlchemy (`flask_sqlalchemy`)                     |
| DB        | Postgres on Render (prod) · SQLite (local + CI)     |
| Templates | Jinja2 (ships with Flask)                           |
| Styling   | Plain CSS in `static/css/styles.css`                |
| JS        | Vanilla JS in `static/js/app.js` (no libraries)     |
| WSGI      | Gunicorn                                            |
| Deploy    | Render via `render.yaml` (push-to-deploy on `main`) |
| CI        | GitHub Actions (lint + boot smoke test on every PR) |

---

## Mapping to the Option A brief

| Requirement (from the Guidelines)    | Where in this repo                                     |
|--------------------------------------|--------------------------------------------------------|
| Event information page               | `routes.home` → `templates/home.html`                  |
| Registration form                    | `routes.register` → `templates/register.html`          |
| Database to store registrations      | `models.py` — `Event` + `Registration` (SQLAlchemy)   |
| List of registered participants      | `routes.participants` → `templates/participants.html`  |
| Detail page for each registration    | `routes.detail` → `templates/detail.html`              |
| Edit or cancel a registration        | `routes.edit` / `routes.cancel` / `routes.restore`     |
| Basic HTML/CSS styling               | `templates/base.html` + `static/css/styles.css`        |
| At least one JavaScript interaction  | `static/js/app.js` (live character counter)            |
| Two related tables                   | `Registration.event_id` → `Event.id` (foreign key)     |
| README                               | this file                                              |
| Short report (≤8 pages)              | [`docs/Short_Report.md`](docs/Short_Report.md)         |
| Video demonstration (≤7 min)         | the MP4 ships inside the Moodle ZIP as `docs/Video_Demo.mp4`                |
| AI-use statement                     | [`docs/AI_USE_STATEMENT.md`](docs/AI_USE_STATEMENT.md) |
| Individual contribution              | [`docs/Individual_Contribution.csv`](docs/Individual_Contribution.csv) |

---

## Run it locally

```bash
# 1. Clone
git clone https://github.com/MichaelNewham/pydublin-workshop-registration
cd pydublin-workshop-registration

# 2. Virtualenv
python -m venv .venv && source .venv/bin/activate

# 3. Install
pip install -r requirements.txt

# 4. Run
python run.py
# → http://localhost:5000
```

On first boot the schema is auto-created and a demo Event plus two sample
registrations are seeded (`event_registration/seed.py`), so the home and
participants pages are non-empty without any setup. Optionally override the
shared organiser password with `ORGANISER_PASSWORD=...` and the database
with `DATABASE_URL=postgresql://...` (see `.env.example`).

### Routes

| Method | Path                              | Purpose                          |
|--------|-----------------------------------|----------------------------------|
| GET    | `/`                               | Event information page           |
| GET    | `/register`                       | Show the registration form       |
| POST   | `/register`                       | Create a registration            |
| GET    | `/registration/<id>`              | Detail page for one registration |
| GET    | `/login`                          | Shared-password login (organiser) |
| POST   | `/login` · `/logout`              | Sign in / sign out               |
| GET    | `/participants`                   | List all active registrations (organiser) |
| GET    | `/registration/<id>/edit`         | Show the edit form (organiser)   |
| POST   | `/registration/<id>/edit`         | Save edits (organiser)           |
| POST   | `/registration/<id>/cancel`       | Cancel — soft-delete (organiser) |
| POST   | `/registration/<id>/restore`      | Restore a cancelled one          |

---

## Project structure

```
Project/
├── event_registration/          # the Flask app
│   ├── __init__.py              #   create_app() factory + auto-seed
│   ├── config.py                #   env-driven configuration
│   ├── extensions.py            #   db = SQLAlchemy()
│   ├── models.py                #   Event + Registration models
│   ├── routes.py                #   all HTTP routes + validation
│   ├── auth.py                  #   shared-password organiser gate
│   ├── seed.py                  #   idempotent first-boot seed
│   ├── templates/*.html         #   Jinja2 templates (8 pages)
│   └── static/{css,js}/         #   styles.css + app.js (the JS interaction)
├── data/seed_events.csv         # matches seed_demo_data()
├── docs/
│   ├── Short_Report.md          # the ≤8-page report (export to PDF)
│   ├── AI_USE_STATEMENT.md
│   ├── Individual_Contribution.csv  # the 30/25/25/20 split
│   └── screenshots/             # embedded in the report
├── run.py                       # `python run.py` entry point
├── requirements.txt
├── render.yaml · Procfile · .env.example
└── .github/workflows/ci.yml     # GitHub Actions: lint + boot smoke test
```

---

## Team & contribution

| Block | Owner            | Role                | %   |
|-------|------------------|---------------------|----:|
| A — Backend & Data     | Michael Newham   | SQLAlchemy models, Flask routes, server-side validation, organiser auth gate | 30% |
| B — Templates          | Sergiu D         | Jinja2 templates, day-of schedule, accessibility pass (page titles, aria-labels, table scopes) | 25% |
| C — Theme, CSS & JS    | Paul Sealy       | `styles.css` print stylesheet, `aria-live` accessibility pass on the JS char counter | 25% |
| D — Docs, Testing & PM | Alessandro Genco | Report finalisation, re-shooting outstanding screenshots, contribution CSV evidence, release QA | 20% |

Full per-student evidence (PRs, files) in
[`docs/Individual_Contribution.csv`](docs/Individual_Contribution.csv) and
[`AUTHORS.md`](AUTHORS.md).

### Coordination trail (Pull Requests)

Every change landed on `main` via PR + CI; nothing bypassed review.

| #    | Title                                                           | Author        | Block |
|------|-----------------------------------------------------------------|---------------|-------|
| [#1](https://github.com/MichaelNewham/pydublin-workshop-registration/pull/1) | Gate organiser routes + remove clipboard (privacy fix) | MichaelNewham | A |
| [#2](https://github.com/MichaelNewham/pydublin-workshop-registration/pull/2) | Add day-of schedule to home page                        | durnescus     | B |
| [#3](https://github.com/MichaelNewham/pydublin-workshop-registration/pull/3) | Complete template usability + accessibility              | durnescus     | B |
| [#4](https://github.com/MichaelNewham/pydublin-workshop-registration/pull/4) | Print stylesheet + aria-live on char counter             | sealymonster  | C |
| [#5](https://github.com/MichaelNewham/pydublin-workshop-registration/pull/5) | Fill Individual_Contribution.csv with PR evidence        | alexg3189     | D |
| [#7](https://github.com/MichaelNewham/pydublin-workshop-registration/pull/7) | Land Block D screenshots + align report/CSV/script       | MichaelNewham | D |

Full PR catalog: <https://github.com/MichaelNewham/pydublin-workshop-registration/pulls?q=is%3Apr>

---

## Production deployment

The live URL is served by **Render** (free tier) using `render.yaml`:

- Every `git push` to `main` triggers an auto-redeploy.
- The production database is **PostgreSQL** (so registrations persist
  across redeploys, unlike the ephemeral SQLite-on-Render default). The
  connection string is held in the Render dashboard as `DATABASE_URL`.
- Local dev and CI automatically fall back to SQLite when `DATABASE_URL`
  is unset, so no extra setup is needed to clone-and-run.

Deploy history (public): <https://dashboard.render.com/web/srv-d993mf77f7vs739o8q7g/deploys>

---

## License & attribution

Academic project for **D4B — Elective 2: Business Programming**.
Code © the four authors listed in [`AUTHORS.md`](AUTHORS.md). "PyCon
Ireland" and Python branding are mentioned for context only and are
trademarks of their respective owners; no affiliation is implied.
