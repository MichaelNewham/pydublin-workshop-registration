# AI-Use Statement

*As required by the project guidelines: "The use of AI tools is allowed, but
it must be explained." This statement is also mirrored in the final report's
"AI-use statement" section.*

## Tools used

- **GitHub Copilot (Chat mode)** — scaffolding, code generation, documenting
- **Anvil AI assistant** (in the Anvil cloud IDE) — component suggestions
- **ChatGPT / Claude** (optional, as the group prefers) — proofreading, email drafts

## Tasks AI assisted with

1. **Initial project scaffold** — directory layout, `anvil.yaml` config,
   `db_schema` for the `Event` and `Registration` tables.
2. **Server-side CRUD functions** — drafts of `create_registration`,
   `update_registration`, `cancel_registration` in `ServerModule1.py`.
3. **Form Python** — wire-up of button handlers and navigation between Forms.
4. **CSS theme** — first draft of `theme.css` and `standard-page.html` shell.
5. **Documentation** — README, this AI-use statement, and the short report
   outline.

## What the group accepted

- The overall folder structure (`client_code` / `server_code` / `theme`) —
  matches the official Anvil Python Directory Structure doc.
- The YAML layout for `anvil.yaml` (services, `db_schema`, `native_deps`).
- The soft-delete pattern for cancellation (status = `'cancelled'` instead of
  a hard delete, preserving the audit trail).

## What the group corrected or rejected

- **Validation rules** — the AI's first draft of `create_registration` did not
  catch duplicate emails or sold-out events; the team added those checks
  explicitly after writing test cases.
- **JS interaction** — the AI initially proposed a jQuery clipboard library;
  we replaced it with the modern `navigator.clipboard` API (no extra dep).
- **Login** — the AI suggested per-user accounts; we deferred that to
  "future improvements" to keep scope realistic for the deadline.

## What the group learned

- AI accelerates boilerplate (config files, CRUD fns, CSS) significantly.
- It does **not** replace domain-specific validation — those came from us
  knowing the business rules (capacity, no duplicate emails).
- An Anvil project is just Python + YAML + HTML/CSS, so AI code edit
  suggestions and human review land cleanly in git diffs.

## Responsibility

The group has read, tested, and validated every line of code in this repo.
The acceptance criteria in `docs/Short_Report.md` § "Testing evidence" were
checked by hand before submission.
