# Short Report — PyDublin Workshop 2026: Event Registration System

> Final length: **target 8 pages** (excluding this markdown's front matter and
> appendices). Export to PDF before submission.
> Group members should fill the `[TODO]` placeholders.

---

## Cover page

- **Project title:** PyDublin Workshop 2026 — Event Registration System
- **Course:** D4B — Elective 2: Business Programming
- **Option:** A - Event Registration Web App
- **Group members:**
  - Michael Newham (261012020) - Block A: Backend & Data (30%)
  - Sergiu D (261024894) - Block B: Client Forms (25%)
  - Paul Sealy (261018041) - Block C: Theme, CSS & JS (25%)
  - Alessandro Genco (262016773) - Block D: Docs, Testing & PM (20%)
- **Date:** `[TODO submission date]`
- **Live app:** https://pydublin-workshop-registration.onrender.com

---

## 1. Business problem

*~½ page*

[TODO] A small community workshop (40 seats) needs a registration system that:

- Lets attendees self-register online without contacting an organiser.
- Captures enough info (name, email, phone, company) for name badges and catering.
- Stops overbooking by enforcing the venue capacity.
- Lets the organiser **list**, **view**, **edit**, and **cancel** registrations
  without touching a spreadsheet.

Previously the team used an Excel sheet by email; duplicate sign-ups,
overbookings, and lost edits were common.

## 2. Solution overview

*~1 page*

A web app built with **Python + Flask + SQLAlchemy + SQLite**, with Jinja2
templates, plain CSS, and a small vanilla-JS interaction. The whole project is
version-controlled in git and auto-deploys to Render on every push, so the
tutor gets a stable public URL with zero human steps after the initial setup.

[TODO: insert architecture diagram/screenshot]

### User journeys

- **Attendee:** Home → Register → submit → confirmation ref
- **Organiser:** Home → Participants → click a row → Detail → Edit or Cancel

## 3. Main features

*~1.5 pages*

| Feature                                    | Where (Flask)                                       |
|--------------------------------------------|-----------------------------------------------------|
| Event information page                     | route `GET /` in `routes.py` -> `templates/home.html` |
| Registration form with server validation   | `GET/POST /register` in `routes.py` -> `templates/register.html` |
| Participant list (auto-updating)           | `GET /participants` -> `templates/participants.html` |
| Detail page per registration               | `GET /registration/<id>` -> `templates/detail.html` |
| Edit registration                          | `GET/POST /registration/<id>/edit` -> `templates/edit.html` |
| Cancel / restore registration (soft-delete)| `POST /registration/<id>/cancel` and `/restore` |
| Two related tables (`Event` < `Registration`) | `models.py`: `Event` + `Registration` with FK   |
| Capacity + duplicate-email enforcement     | `register()` in `routes.py` (SQLAlchemy queries)    |
| HTML / CSS styling                          | `templates/base.html` + `static/css/styles.css` |
| JavaScript interaction (clipboard + char counter) | `static/js/app.js`                             |

[TODO: 2–3 annotated screenshots of each major screen]

## 4. Technologies / tools used

*~½ page*

- **Python 3** (3.11+) - the language for both back-end (Flask routes, models)
  and the small client-side JS.
- **Flask** - lightweight WSGI web framework (used in Week 6 of the course).
- **SQLAlchemy** - ORM; declares the two models and their relationship.
- **SQLite** - the database file (`app.db`), created automatically on first run.
- **Jinja2** - HTML templates (ships with Flask).
- **Plain HTML / CSS / vanilla JavaScript** - no external front-end libraries.
- **Git + GitHub** - version control and team collaboration.

Tools for the project itself:

- **GitHub Copilot** - AI pair-programming (see `AI_USE_STATEMENT.md`)
- **Render.com** - push-to-deploy hosting (free tier).
- **GitHub Actions** - CI: compile + boot-test on every PR.

## 5. Database schema

*~½ page*

Two related Data Tables (1-to-many):

```
Event (1) ──────< Registration (N)
                       │ event_id (liveObject link to Event)
```

**Event** columns: `title`, `date`, `location`, `capacity`, `price`, `description`
**Registration** columns: `name`, `email`, `phone`, `company`, `notes`,
                          `status` (registered / cancelled), `created_at`,
                          `event_id` (FK → Event)

Both are declared as SQLAlchemy models in `event_registration/models.py`: `Event`
has a `registrations` relationship; `Registration.event_id` is the foreign key.

## 6. Testing evidence

*~1 page*

We tested each user journey by hand. Log of accepted scenarios:

| # | Scenario                                            | Expected                                   | Pass |
|---|-----------------------------------------------------|--------------------------------------------|------|
| 1 | Open Home with empty DB                              | Demo event auto-creates, page renders      | ✓    |
| 2 | Submit valid registration                            | Row appears in list, confirmation ref shown| ✓    |
| 3 | Submit duplicate email                               | Server blocks with "already registered"    | ✓    |
| 4 | Submit when seats = capacity                         | Server blocks with "sold out"              | ✓    |
| 5 | List participants                                    | All active registrations shown desc by date| ✓    |
| 6 | Edit a registration, save                            | Changes persist after refresh              | ✓    |
| 7 | Cancel a registration                                | Status flips to Cancelled; seat frees up   | ✓    |
| 8 | JS: click "Copy event ref"                           | Ref string on clipboard                    | ✓    |
| 9 | JS: type in notes field                              | Char counter updates live                  | ✓    |
| 10| Refresh Participants after cancelling                | Cancelled row hidden from default view     | ✓    |

[TODO: attach screenshots for the most important scenarios.]

## 7. Limitations & future improvements

*~½ page*

- **No authentication** — anyone with the URL can currently see the participant
  list. Future: use Flask-Login for proper organiser accounts.
- **Single event** — the demo seeds one Event row; multi-event would just need
  a list-detail UI on top of the same schema.
- **No payment** — `price` is informational; future: integrate Stripe via Anvil's
  HTTP API.
- **No automated tests** — manual test log only; future: convert §6 into a
  pytest-driven smoke suite run against the standalone server.

## 8. AI-use statement

*~¼ page*

See [`AI_USE_STATEMENT.md`](AI_USE_STATEMENT.md) for the full statement. In
short: GitHub Copilot was used for scaffolding config files, CRUD functions,
and documentation drafts; the group corrected validation logic and the
JS hook. All code was reviewed and tested by the team before submission.

---

## Appendix A — How to run

See [`README.md`](README.md) for full instructions. TL;DR:

```bash
pip install -r requirements.txt
python run.py
# open http://localhost:5000
```

Or on Render: `git push` to `main` triggers auto-deploy via the `render.yaml`.
