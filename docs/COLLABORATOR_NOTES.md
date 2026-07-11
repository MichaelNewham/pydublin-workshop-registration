# Collaborator notes

> Hello team. This is your one-page guide to working on the PyDublin Workshop
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

You own the data model and all server-side logic.

**Your files:**
- `event_registration/models.py` (the `Event` and `Registration` SQLAlchemy classes)
- `event_registration/routes.py` (the 9 URL routes + validation)
- `event_registration/seed.py` (idempotent first-boot seeding)
- `event_registration/config.py` (env-driven settings)
- `event_registration/extensions.py` + `event_registration/__init__.py` (app factory)

**Typical tasks:**
- Add a new column to a model (e.g. "dietary requirements" on `Registration`):
  edit `models.py`, then add the column to the `register.html` form so Sergiu
  sends it through.
- Tighten validation in `routes.register` (the function with the `@bp.route`
  decorator).
- Add a new route.

**Workflow tips:**
- After editing models, **delete `event_registration/app.db`** locally to let
  the schema rebuild itself - we don't run migrations for this demo.
- Run the smoke test before pushing: open the Python REPL and
  `from event_registration import create_app; app = create_app();
  c = app.test_client(); print(c.get('/').status_code)` should print `200`.

---

### 🟦 Sergiu D - Block B: Templates (25%)

You own every HTML page.

**Your files (all under `event_registration/templates/`):**
- `base.html` - the shared shell (header / footer / CSS / JS includes). Edit
  this to change the brand mark or global nav.
- `home.html` - the event information page (the first thing visitors see).
- `register.html` - the registration form.
- `participants.html` - the organiser's list.
- `detail.html` - one registration's detail page.
- `edit.html` - the edit form.
- `error.html` - 404 / 500 fallback.

**Typical tasks:**
- Add an empty-state illustration to `participants.html` (when nobody has
  registered yet).
- Add a "registered at" timestamp column to the participants table.
- Tighten the layout of `register.html`.

**Workflow tips:**
- Jinja2 syntax: `{% if condition %}`, `{% for x in items %}`,
  `{{ variable }}`. Ask Michael if you need a new variable passed in from
  the route.
- Don't repeat the header / footer in each page - they live in `base.html`.
  Each child page starts with `{% extends "base.html" %}`.
- Watch out: the `<textarea>` in `register.html` and `edit.html` has the
  JS character counter wired to its sibling `.js-notes-counter`. If you
  move one, keep them adjacent.

---

### 🟪 Paul Sealy - Block C: CSS & JavaScript (25%)

You own the look and the one required JS interaction.

**Your files:**
- `event_registration/static/css/styles.css` (~260 lines, single source of truth for styling)
- `event_registration/static/js/app.js` (the clipboard copy + the character counter)

**Typical tasks:**
- Re-theme the palette (change the CSS custom properties at the top: `--brand`,
  `--accent`, etc.) - one-place colours everything.
- Improve the responsive breakpoint (currently kicks in at 640px).
- Add a subtle hover animation to the table rows in `participants.html`.
- Polish the JS feedback (e.g. the "Copied: XXX" tooltip duration).

**Workflow tips:**
- I've used CSS custom properties (`:root { --brand: #1a7a3a; }`) - change
  them and the whole app re-themes. Avoid hardcoding colours further down.
- `app.js` is a single IIFE - it binds to anything with class `.js-copy-ref`
  and any `.js-notes-counter` sibling of a `<textarea>`. If Sergiu renames
  those classes, the JS breaks; coordinate with him.
- You can edit the CSS freely without coordinating - it's a single file.

---

### 🟧 Alessandro Genco - Block D: Docs, Testing & PM (20%)

You own everything that isn't running code. This is the deployment + the
deliverables the tutor will grade directly.

**Your files:**
- `README.md` - the repo's front door.
- `docs/Short_Report.md` - the <=8-page report (still has `[TODO]` slots for
  screenshots + final date).
- `docs/Video_Demo_script.md` - the shot list for the 7-minute demo.
- `docs/Individual_Contribution.csv` - the grade-weighting sheet.
- `docs/AI_USE_STATEMENT.md` - the transparency statement (already written).
- `docs/CI_SETUP.md`, `docs/COLLABORATOR_NOTES.md` (this file).
- `render.yaml` (the Render deploy config - already working, only touch if
  the deploy needs to change).

**Typical tasks:**
- **Screenshots**: visit the live app, screenshot Home / Register / List /
  Detail / Edit, drop them into `docs/screenshots/`, embed in `Short_Report.md`.
- **Report PDF**: when the markdown is final, `pandoc docs/Short_Report.md
  -o docs/Short_Report.pdf` or just print to PDF from VS Code.
- **Demo video**: follow `docs/Video_Demo_script.md`. Loom / OBS / QuickTime
  all work. Keep under 7 minutes.
- **Final QA pass**: walk the live URL through every scenario in
  `Short_Report.md` section 6 + tick each box.

**Workflow tips:**
- You're also the **release manager**. Before the submission, run a last
  pass: confirm CI is green, the live URL works from a private tab, the
  README's live URL matches, no `[TODO]` is left in the report.
- Build the **Moodle submission ZIP** last: `zip -r submission.zip . -x
  '.git/*' '.venv/*' '__pycache__/*'` from inside the project folder.

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
