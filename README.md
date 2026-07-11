# PyDublin Workshop 2026 — Event Registration System

A low-code / no-code business app built with **Anvil** (pure Python front-end
and back-end), for the **D4B — Elective 2: Business Programming** final project
(**Option B**).

> Read [`Project_Overview.md`](Project_Overview.md) and `Project - Business
> Programming May 2026 - Guidelines.pdf` for the official brief. This README
> explains **how to run** the app locally and how the project is organised.

---

## What it does

A simple but complete event-registration tool for a small workshop:

- **Event information page** — date, location, description, price, seats remaining
- **Registration form** — name, email, phone, company, notes (with email
  uniqueness + capacity checks enforced on the server)
- **List of participants** for the organiser, refreshed on demand
- **Detail page** per registration, with edit / cancel / restore actions
- **Two related Data Tables** — `Event` ↔ `Registration` (1-to-many link)
- **HTML / CSS styling** via a custom theme + the Inter typeface
- **One JavaScript interaction** — copy-to-clipboard of an event ref, plus a
  live character counter on the notes textarea (see `anvil.yaml` → `native_deps`)

## Tech stack

| Layer      | Tech                                     |
|------------|------------------------------------------|
| Front-end  | Anvil drag-and-drop designer, Python 3   |
| Back-end   | Anvil Server Modules (`@anvil.server`)   |
| Database   | Anvil Data Tables (SQLite under the hood)|
| Styling    | `theme.css`, `standard-page.html`, roles |
| JS hook    | `native_deps.head_html` in `anvil.yaml`  |

No `pyproject.toml` / `requirements.txt` — Anvil apps declare their
dependencies in `anvil.yaml`, not in pip/PEP 517 files.

---

## Repository layout

```
Project/
├── event_registration/            ← the Anvil app (top-level Python package)
│   ├── __init__.py
│   ├── anvil.yaml                 ← app metadata + DB schema + JS native_deps
│   ├── client_code/               ← Forms (UI + client Python)
│   │   ├── Home/                  ← event information page (startup Form)
│   │   ├── RegistrationForm/      ← registration form (POSTs to DB)
│   │   ├── ParticipantsListForm/  ← list for organisers (+ RepeatingPanel item)
│   │   ├── RegistrationDetailForm/← detail page per registration
│   │   └── EditRegistrationForm/  ← edit + cancel/restore
│   ├── server_code/
│   │   └── ServerModule1.py       ← callable CRUD fns, validation, capacity
│   └── theme/
│       ├── assets/
│       │   ├── standard-page.html ← HTML shell + <script> JS hook
│       │   └── theme.css          ← global CSS styling
│       ├── parameters.yaml        ← roles + colour scheme
│       └── templates.yaml
│
├── data/
│   └── seed_events.csv            ← seed rows (also seeded automatically)
│
└── docs/
    ├── Short_Report.md            ← source of the 8-page report
    ├── Video_Demo_script.md       ← <=7-min demo shotlist
    ├── Individual_Contribution.csv← mirrors Group_Evaluation.pdf
    └── screenshots/               ← add UI screenshots here
```

Each Form is a Python package with two files:

| File                  | What it holds                                              |
|-----------------------|------------------------------------------------------------|
| `__init__.py`         | The Python code you see in Anvil's Code View for that Form |
| `form_template.yaml`  | The visual layout (components, properties, event bindings) |

---

## How to run

### Option 1 — Standalone Anvil App Server (offline / local)

The Anvil runtime is open source and ships as a Docker image, so you can run
the app fully offline once Docker is installed.

```bash
# 1. Pull the app-server image (one-time, ~500 MB):
docker pull anvil/anvil-app-server

# 2. From THIS directory (where this README lives), launch:
docker run --rm -it \
    -p 3030:3030 \
    -v "$PWD:/app" \
    -w /app \
    anvil/anvil-app-server

# 3. Open http://localhost:3030 in a browser.
```

On first launch, the server reads `event_registration/anvil.yaml`, builds the
SQLite database in `.anvil-data/` (git-ignored), and seeds the default event
the first time `HomeForm` calls `get_or_create_demo_event()`.

### Option 2 — Anvil cloud IDE (recommended for team collaboration)

1. Sign up (free) at https://anvil.works.
2. **File → Clone from Git**, paste **this repo's URL**, branch `main`.
3. Anvil imports the `event_registration` folder as a normal app.
4. Click **Run** in the top-right.

This is the easiest path for a 4-person group: everyone gets the visual
designer, simultaneous editing, and one-click sharing.

---

## Decisions and assumptions

These are **easy to change** — listed here so nothing is hidden. Open an issue
or edit the relevant file directly if you want to tweak.

| Decision           | Value                                            | Where               |
|--------------------|--------------------------------------------------|---------------------|
| Platform           | Anvil (pure Python front+back end)               | (chosen)            |
| Event type         | Workshop                                         | `data/seed_events.csv` |
| Event name         | PyDublin Workshop 2026 — Python for Business     | `anvil.yaml` / DB   |
| Registration fields| name, email, phone, company, notes               | `anvil.yaml` UI     |
| Login              | (none yet — added as a future improvement)        | n/a                 |
| Team (blocks)      | Michael Newham (261012020, A, 30%),                | `docs/Individual_Contribution.csv`, |
|                    | Sergiu D (261024894, B, 25%),                       | `AUTHORS.md` |
|                    | Paul Sealy (261018041, C, 25%),                     |                     |
|                    | Alessandro Genco (262016773, D, 20%)                |                     |
| Git remote         | `MichaelNewham/pydublin-workshop-registration` (private) | `.git/`        |

---

## Development workflow (small team, 4 people)

The project is split into four functional blocks that together cover the
entire repo. The split mirrors the Group_Evaluation.pdf role template
(database/backend 30%, interface/design 25%, testing/docs 25%,
integration/PM 20%):

| Block | Owner              | Role                  | Owns                                                              | %   |
|-------|--------------------|-----------------------|-------------------------------------------------------------------|-----|
| **A** | Michael Newham     | Backend & Data        | `anvil.yaml` db_schema, `server_code/ServerModule1.py` (CRUD + validation) | 30% |
| **B** | Sergiu D           | Client Forms          | All `client_code/*` Forms (Home, Registration, List, Detail, Edit) + form logic + navigation | 25% |
| **C** | Paul Sealy         | Theme, CSS & JS       | `theme/` (HTML shell + CSS roles) + `native_deps` JS interaction   | 25% |
| **D** | Alessandro Genco   | Docs, Testing & PM    | `docs/` + `README.md` + AI-use statement + demo video + git integration + final QA | 20% |

### Build order

1. **A (Michael)** lands the db_schema + `@anvil.server.callable` CRUD functions first - every other block calls into these.
2. **B (Sergiu)** builds the five Forms on top of A's callables, wiring navigation and form validation.
3. **C (Paul)** can start in parallel with B - the CSS roles are just classes Form YAML references. Adds the `native_deps` JS hook in `anvil.yaml` (co-owned with A via PR).
4. **D (Alessandro)** drafts `docs/` alongside A/B/C; writes the test log as features land; records the demo video and does final QA last.

The blocks are not strictly sequential - A is the only hard prerequisite
(B's Forms need A's callables). See `docs/Individual_Contribution.csv`
for the canonical, submission-ready percentage split.

---

## Mapping to course requirements (Option A = Option B deliverables)

| Requirement (Guidelines PDF)         | Where in this repo                          |
|--------------------------------------|---------------------------------------------|
| Event information page               | `client_code/Home/`                         |
| Registration form                    | `client_code/RegistrationForm/`             |
| Database to store registrations      | Data Tables `Event` + `Registration` in `anvil.yaml` |
| List of registered participants      | `client_code/ParticipantsListForm/`         |
| Detail page for each registration    | `client_code/RegistrationDetailForm/`       |
| Edit or cancel a registration        | `client_code/EditRegistrationForm/` + `cancel_registration()` in `ServerModule1.py` |
| Basic HTML/CSS styling               | `theme/assets/standard-page.html` + `theme.css` |
| At least one simple JS interaction   | `native_deps.head_html` in `anvil.yaml`     |
| Two related tables                   | `Registration.event_id` → `Event` (liveObject FK) |
| README                               | this file                                   |
| AI-use statement                     | `docs/AI_USE_STATEMENT.md` (linked from report) |
