# Short Report — PyDublin Workshop 2026: Event Registration System

> Final length: **target 8 pages** (excluding this markdown's front matter and
> appendices). Export to PDF before submission.
> Group members should fill the `[TODO]` placeholders.

---

## Cover page

- **Project title:** PyDublin Workshop 2026 — Event Registration System
- **Course:** D4B — Elective 2: Business Programming
- **Option:** B — Low-Code / No-Code Business App
- **Group members:**
  - Michael Newham (261012020) - Block A: Backend & Data (30%)
  - Sergiu D (261024894) - Block B: Client Forms (25%)
  - Paul Sealy (261018041) - Block C: Theme, CSS & JS (25%)
  - Alessandro Genco (262016773) - Block D: Docs, Testing & PM (20%)
- **Date:** `[TODO submission date]`

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

A low-code app built with **Anvil** (pure Python front-end and back-end).
The app is a single deployment unit (no separate API server to maintain), and
all logic lives in version-controlled Python + YAML files.

[TODO: insert architecture diagram/screenshot]

### User journeys

- **Attendee:** Home → Register → submit → confirmation ref
- **Organiser:** Home → Participants → click a row → Detail → Edit or Cancel

## 3. Main features

*~1.5 pages*

| Feature                                    | Where                                               |
|--------------------------------------------|-----------------------------------------------------|
| Event information page                     | `client_code/Home/`                                 |
| Registration form with server validation   | `client_code/RegistrationForm/` + `create_registration()` |
| Participant list (auto-updating)           | `client_code/ParticipantsListForm/`                 |
| Detail page per registration               | `client_code/RegistrationDetailForm/`               |
| Edit registration                          | `client_code/EditRegistrationForm/` + `update_registration()` |
| Cancel / restore registration (soft-delete)| `cancel_registration()` / `restore_registration()`  |
| Two related Data Tables (`Event`↔`Registration`) | `anvil.yaml` → `db_schema`               |
| Capacity + duplicate-email enforcement     | `create_registration()` in `ServerModule1.py`       |
| HTML / CSS styling                          | `theme/assets/standard-page.html` + `theme.css`     |
| JavaScript interaction (clipboard + char counter) | `native_deps.head_html` in `anvil.yaml`      |

[TODO: 2–3 annotated screenshots of each major screen]

## 4. Technologies / tools used

*~½ page*

- **Anvil** — low-code Python web app platform (front-end + back-end + Data
  Tables in one tool)
- **Python 3** — only language used (per the course's Python focus)
- **SQLite** — under the hood of Anvil Data Tables
- **YAML** — config (`anvil.yaml`, `parameters.yaml`)
- **Standard HTML / CSS / JS** — the theme shell (`standard-page.html`,
  `theme.css`, the inline `<script>` namespace)
- **Git** — version control and team collaboration

# Tools for the project itself:

- **GitHub Copilot** — AI pair-programming (see `AI_USE_STATEMENT.md`)
- **Docker** — local run via `anvil/anvil-app-server`

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

Both are declared in `event_registration/anvil.yaml` under `db_schema:`.

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
  list. Future: use Anvil's built-in Users service for organiser accounts.
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
docker run --rm -it -p 3030:3030 -v "$PWD:/app" -w /app anvil/anvil-app-server
# open http://localhost:3030
```
