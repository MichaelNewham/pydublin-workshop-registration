# Collaborator notes

> Hello team. This is your one-page guide to working on the PyCon Ireland
> 2026 Event Registration System. Each of you has a specific **block** of
> files to own; this doc tells you exactly what to touch and how to push
> changes safely. Read the **Common setup** section once, then jump to
> **Your block**.

---

## Live links you'll need

| What | URL |
|------|-----|
| **GitHub repo** (your code)      | https://github.com/MichaelNewham/pydublin-workshop-registration |
| **Live app** (running on Render) | https://pydublin-workshop-registration.onrender.com |
| **CI runs** (green = good)       | https://github.com/MichaelNewham/pydublin-workshop-registration/actions |
| **Render dashboard** (owner only)| https://dashboard.render.com/web/srv-d993mf77f7vs739o8q7g |

> The live app sleeps when idle. First visit after a quiet period may take
> up to ~50 s to cold-start. After that it's fast.

---

## Blocks at a glance

| Block | Owner            | Owns                                                                  |
|-------|------------------|-----------------------------------------------------------------------|
| A     | Michael Newham   | `event_registration/models.py`, `routes.py`, `seed.py`, `config.py`  |
| B     | Sergiu D         | `event_registration/templates/*.html`                                 |
| C     | Paul Sealy       | `event_registration/static/css/styles.css`, `static/js/app.js`        |
| D     | Alessandro Genco | `README.md`, `docs/*`, `render.yaml`, demo video, final QA           |

Stay in your block. If you need a change in someone else's block,
**open a PR** for it (instructions below) - don't push straight to `main`.

---

## Common setup (do once)

You'll need a free GitHub account and Python 3.10+ on your laptop.

### 1. Accept the repo invite

Michael will send an invite to your GitHub username. The email from GitHub
will say "You've been invited to collaborate on
MichaelNewham/pydublin-workshop-registration". Click **Accept invitation**.

### 2. Clone the repo

```bash
git clone https://github.com/MichaelNewham/pydublin-workshop-registration
cd pydublin-workshop-registration
```

### 3. Make a virtualenv and install dependencies (one-time)

```bash
python3 -m venv .venv
source .venv/bin/activate         # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Run the app locally

```bash
python run.py
# -> open http://localhost:5000
```

The first run auto-creates the SQLite DB and seeds a demo event + 2 sample
registrations. The home page won't be empty.

---

## How to make a change (the Pull Request flow)

Please **don't** commit straight to `main`. Use a branch so CI can check
your change before it lands.

```bash
# 1. Always start from the latest main
git checkout main
git pull

# 2. Create a branch named after your block + what you're doing
git checkout -b sergiu/improve-home-layout

# 3. Edit your files. Save them.

# 4. Stage and commit
git add event_registration/templates/home.html        # <- your file(s)
git commit -m "ui(home): tighten title spacing on small screens"

# 5. Push the branch to GitHub
git push -u origin sergiu/improve-home-layout

# 6. Open the Pull Request (either click the URL git prints, or:)
gh pr create --title "Tighten title spacing" --body "Small CSS adjustment for mobile."
```

GitHub will now run the CI workflow on your branch (~20 s). When the green
tick appears, click **Merge pull request** on GitHub. Render will then
auto-deploy your merged change (~1-2 min) and the live app will update.

### Branch naming convention

`<your-first-name>/<short-slug>` is plenty. Examples:

- `michael/add-restore-route`
- `sergiu/add-empty-state`
- `paul/clipboard-feedback`
- `alessandro/report-screenshots`

### If CI fails on your PR

Click the red ❌ on GitHub, read the failing step, fix locally, then:

```bash
git add <fixed-files>
git commit -m "fix: address CI failure"
git push             # same branch - the PR updates automatically
```

---

## Your block (read the one with your name)

### 🟩 Michael Newham - Block A: Backend & Data (30%)

You own the data model and all server-side logic. **Michael has already done
one PR** - read this section as a worked example of how his block works in
practice, not as a TODO list.

**Files you own:**
- `event_registration/models.py` (the `Event` and `Registration` SQLAlchemy classes)
- `event_registration/routes.py` (every URL route + validation)
- `event_registration/seed.py` (idempotent first-boot seeding)
- `event_registration/config.py` (env-driven settings)
- `event_registration/extensions.py` + `event_registration/__init__.py` (app factory)
- `event_registration/auth.py` (the shared-password organiser gate)

### Worked example: PR #1 (merged 11 July 2026)

Michael's first change was a real fix prompted by a design review: the
organiser-only Participants list was reachable from a public button on the
home page, exposing attendee names, emails, phones, and notes to anyone on
the internet. He turned it into a PR. Real steps:

1. Set local git identity (so commits come out under his name):
   ```bash
   git config user.name  "Michael Newham"
   git config user.email "261012020@digital4business.eu"
   ```

2. Pulled latest `main` and branched:
   ```bash
   git checkout main && git pull
   git checkout -b michael/organiser-gate-and-cleanup
   ```

3. Built the fix entirely inside his own block:
   - New `event_registration/auth.py` - shared-password gate using the
     `ORGANISER_PASSWORD` env var (default `pydublin-2026`), plus a
     `@login_required` decorator.
   - Two new routes in `routes.py`: `GET/POST /login` and `POST /logout`.
   - Applied `@login_required` to `participants()`, `edit()`, `cancel()`,
     `restore()`. Left `detail()` public so attendees can still see their
     own post-register confirmation page.
   - Cross-block touches (templates + CSS + JS) were coordinated via PR -
     not bypassed - because they live in other people's blocks.

4. Pushed the branch and opened the PR:
   ```bash
   git push -u origin michael/organiser-gate-and-cleanup
   gh pr create --title "fix(ui+auth): gate organiser routes + remove clipboard" --body "..."
   ```

5. **CI caught a regression** - the smoke test asserted `GET /participants`
   would return 200, but the new gate correctly returns 302. Michael
   didn't argue with the assertion; he updated `ci.yml` to authenticate
   against the gate before checking the route, plus added wrong-password
   + logout cases. Pushed the fix. CI went green.

6. Merged PR #1 on GitHub. Render auto-deployed in 54 seconds. Michael
   verified the fix on the live URL via curl (anonymous `/participants`
   → 302 to `/login`; authed → 200).

Read the full PR (diff + discussion + CI run) at:
https://github.com/MichaelNewham/pydublin-workshop-registration/pull/1

### Tips for next time Michael opens a PR

- For route changes that affect gated pages, also update the CI smoke
  test in `.github/workflows/ci.yml` in the same commit - it'll save you
  the "CI red on first push" round-trip.
- After editing `models.py`, delete `event_registration/app.db` locally
  so the schema rebuilds itself on next boot (we don't run Alembic).
- After deploying, verify on the live URL (`https://pydublin-workshop-registration.onrender.com`)
  in a private browser tab - the cookie state there can surprise you.
- Smoke test before pushing:
  ```bash
  python -c "
  from event_registration import create_app
  app = create_app()
  c = app.test_client()
  assert c.get('/').status_code == 200
  print('OK')
  "
  ```

---

### 🟦 Sergiu D - Block B: Templates (25%)

You own every HTML page. Your first PR has been pre-scoped - see below.

**Files you own (all under `event_registration/templates/`):**
- `base.html` - the shared shell (header / footer / CSS / JS includes).
- `home.html` - the event information page (the first thing visitors see).
- `register.html` - the registration form.
- `participants.html` - the organiser's list.
- `detail.html` - one registration's detail page.
- `edit.html` - the edit form.
- `error.html` - 404 / 500 fallback.

### Suggested first PR: "Add a day-of schedule section to the home page"

The current home page shows event title + date + price + a Register button.
The brief doesn't ask for a schedule, but adding a simple **itinerary**
makes the app feel like a real conference site and is a natural extension
of "event information page". Anchor it to a real event so the content
isn't invented:

**Source:** Python Ireland hosts an actual **PyCon Ireland 2026** on
**Saturday 17 October at Trinity College Dublin** (see https://python.ie/
for the public announcement). Use that as the model: a workshop / single-
track day with ~5 sessions and breaks.

**What to build**
- A new section in `home.html` (below the existing `.event-card`) called
  something like `.schedule-section` with a `<table>` of times + sessions,
  plus a short intro line. Suggested rows:
  ```
  09:00  Registration + coffee
  09:30  Keynote: Python in Irish business (TBC)
  10:30  Talk: pandas for business reporting
  11:15  Coffee break
  11:30  Workshop: building a Flask web app (hands-on)
  13:00  Lunch (provided)
  14:00  Talk: scraping competitor prices ethically
  15:00  Lightning talks
  16:00  Wrap-up + networking
  ```
- All content lives entirely in `home.html` as static prose - you don't
  need a new model or route for v1. (If you want database-backed sessions
  later, ask Michael via a Block A coordination PR.)
- Give the section a heading + an intro line like:
  > "Provisional schedule for PyCon Ireland 2026 - subject to change."
  This is honest and protects you if python.ie shifts the agenda later.

**Branch and PR name**
- Branch: `sergiu/home-schedule-section`
- Commit message: `ui(home): add day-of schedule section (PyCon IE 2026 model)`
- PR title: `Add day-of schedule to home page`

**Coordinate with**
- **Paul (C)** will restyle your `<table>` via `styles.css`; just use
  sensible semantic classes (e.g. `.schedule-table` with `<th>` for
  "Time" / "Session"). Paul will theme it.
- **Michael (A)** if you also need the event *title + date* to say
  "PyCon Ireland 2026, 17 October, Trinity College Dublin" - those
  values live in `seed.py` (Block A). Open a small cross-block PR or
  ask Michael to update them in his next commit.

**Don't break**
- The `<textarea>` in `register.html` and `edit.html` has the JS character
  counter wired to its sibling `.js-notes-counter`. If you move one, keep
  them adjacent. (The JS lives in Paul's block.)
- The `{% extends "base.html" %}` pattern stays - keep your new section
  inside `{% block content %}` of `home.html`.

**Workflow tips**
- Jinja2 cheatsheet: `{% if cond %}`, `{% for x in items %}`,
  `{{ variable }}`. Ask Michael if you need a new variable passed from
  the route.
- Don't repeat the header / footer in each page - they live in `base.html`.

After this PR lands, your section here gets rewritten (same as Michael's)
into a worked example for the next person to learn from.

---

### 🟪 Paul Sealy - Block C: CSS & JavaScript (25%)

You own the look-and-feel and the (one) required JavaScript interaction.

**Files you own:**
- `event_registration/static/css/styles.css` (~260 lines, single source of truth for styling)
- `event_registration/static/js/app.js` (~40 lines, just a live character counter after PR #1)

### Suggested first PR: "Rebrand to PyCon Ireland colours + logo"

The current palette is generic green (`--brand: #1a7a3a`). For a
realistic PyCon Ireland demo, re-theme around Python's actual brand:
the language's classic **blue (#306998) + yellow (#FFD43B)** of the
Python logo (which Python Ireland also uses). With attribution, of
course.

**What to build**
- Update the CSS custom properties at the top of `styles.css`:
  ```css
  :root {
    --brand: #306998;       /* Python blue */
    --brand-dark: #1f4d75;
    --accent: #FFD43B;      /* Python yellow */
    /* keep --bg, --surface, --text as-is */
  }
  ```
  This one change re-themes the header mark, primary buttons, focus rings,
  and the price colour across the whole app.
- Save the Python Ireland logo to `static/img/python-ireland-logo.png`
  (create the `static/img/` folder). Right-click the logo at
  https://python.ie/ - save PNG. Roughly 80x80 px is fine.
- Edit `templates/base.html` to display the logo in the header (next to
  the brand mark) using:
  ```html
  <img src="{{ url_for('static', filename='img/python-ireland-logo.png') }}"
       alt="Python Ireland" class="brand-logo" />
  ```
  Plus a CSS rule for `.brand-logo` (something like `height: 32px;
  vertical-align: middle; margin-right: 8px;`).
- Edit `templates/base.html` footer to add the attribution line:
  > `Logo \u00a9 Python Ireland, used here for an academic project demo.`

**Branch and PR name**
- Branch: `paul/rebrand-pycon-ireland`
- Commit message: `style: rebrand to PyCon Ireland palette + logo (with attribution)`
- PR title: `Rebrand to PyCon Ireland colours and add logo`

**Coordinate with**
- **Sergiu (B)** - if he lands his schedule-section first, theme his
  `.schedule-table` so it matches (borders, hover, etc.). If you land
  first, your `--brand` change will already recolour his table headers.
- **Alessandro (D)** - tell him so he can update the report + screenshots
  to show the PyCon rebrand.

**Polish ideas (optional, after the rebrand lands)**
- Improve the responsive breakpoint (currently 640px, may need widening
  for the new schedule table).
- Add a subtle `-webkit-transition` on `.participants-table tbody tr:hover`.
- Tighten the `.field-hint` colour to use `--text-muted` consistently.

**Don't break**
- `static/js/app.js` is a single IIFE that binds to every
  `.js-notes-counter` (the live character counter - this is the **one
  JavaScript interaction** the brief requires; it's already done and
  covered by CI). Don't touch the file unless you have a specific bug to
  fix.
- If Sergiu renames the `.js-notes-counter` class, the JS breaks - he's
  been warned; flag it on his PR if you spot it.

**Workflow tips**
- Change the CSS variables once at the `:root` and the whole site
  re-themes - avoid hardcoding Python blue anywhere else.
- Logo attribution in the footer is non-negotiable for an academic
  project using a real organisation's branding.

---

### 🟧 Alessandro Genco - Block D: Docs, Testing & PM (20%)

You own everything that isn't running code. This is the deployment +
deliverables the tutor will grade directly.

**Files you own:**
- `README.md` - the repo's front door.
- `docs/Short_Report.md` - the <=8-page report (has `[TODO]` slots for
  screenshots + final date).
- `docs/Video_Demo_script.md` - the shot list for the 7-minute demo.
- `docs/Individual_Contribution.csv` - the grade-weighting sheet.
- `docs/AI_USE_STATEMENT.md` - the transparency statement.
- `docs/CI_SETUP.md`, `docs/COLLABORATOR_NOTES.md` (this file),
  `docs/SUBMISSION_CHECKLIST.md`.
- `render.yaml` (the Render deploy config - already working, only touch if
  the deploy needs to change).

### Suggested first PR: "Refresh report + README to match PyCon rebrand"

Once Sergiu (B) and Paul (C) land their PyCon Ireland rebrand PRs, the
report and README will be out of date. Your PR catches them up:

**What to do**
- Update `README.md`'s top description + decisions table:
  - "PyDublin Workshop 2026" -> "PyCon Ireland 2026 (academic demo)"
  - Add a row noting the Python Ireland logo attribution.
- Update `docs/Short_Report.md`:
  - Cover page title + business problem section (align with the
    "registration system for PyCon Ireland 2026" framing).
  - Section 3 "Main features": add a row for the day-of schedule
    section Sergiu built.
  - Section 4 "Technologies": add `static/img/python-ireland-logo.png`
    as a static asset.
- Add a new subsection to `docs/AI_USE_STATEMENT.md` if Paul's rebrand
  used AI to pick colours or write CSS - he should send you a 1-line
  summary of what AI helped with.

**Branch and PR name**
- Branch: `alessandro/report-pycon-rebrand-refresh`
- Commit message: `docs: align README + report with PyCon Ireland rebrand`
- PR title: `Refresh docs to reflect PyCon Ireland rebrand`

**Open-ended tasks (no PR needed, just do them)**
- **Screenshots**: visit the live app after the rebrand + schedule
  section are merged. Screenshot Home (with the new schedule + logo),
  Register, Login, Participants, Detail, Edit. Drop into
  `docs/screenshots/`, embed in `Short_Report.md` section 6.
- **Report PDF**: when markdown is final, `pandoc docs/Short_Report.md
  -o docs/Short_Report.pdf` or browser-print to PDF.
- **Demo video**: follow `docs/Video_Demo_script.md`. Loom / OBS /
  QuickTime all work. **Keep under 7 minutes.**

**Release manager duties (final QA before Moodle submission)**
- Confirm CI is green on the latest `main` commit.
- Live URL works in a private browser tab:
  https://pydublin-workshop-registration.onrender.com
- README's live URL matches the actual deployment.
- No `[TODO]` is left in the report.
- Individual contributions CSV sums to 100%.
- Build the **Moodle submission ZIP** per
  `docs/SUBMISSION_CHECKLIST.md` (not the rough command below; that's
  the canonical one).
- Verify the ZIP opens cleanly on a fresh machine.

**Workflow tips**
- You're the **release manager**. Block submission if anything in the
  SUBMISSION_CHECKLIST fails.
- Schedule your work to land **after** Sergiu + Paul + Michael have
  merged their block work but **before** the submission deadline.
- Your first PR (the docs-refresh) is real software-engineering work,
  not just typing - it's coordinating the team's content after a
  cross-block rebrand.

---

## Where to ask for help

- **Stuck on a technical thing?** Open an issue on GitHub (Issues tab) and
  tag the owner of that block in the title.
- **Live app is down or returning 500s?** Check
  https://dashboard.render.com/web/srv-d993mf77f7vs739o8q7g/deploys
  for the latest deploy log - a red deploy means the last commit to `main`
  broke something.
- **CI is failing on `main`?** That's urgent - it blocks everyone's PRs.
  Ping whoever last merged to `main`.
