# AI-Use Statement

*As required by the project guidelines: "The use of AI tools is allowed, but
it must be explained." This statement is also mirrored in the final report's
"AI-use statement" section.*

## Tools used

- **GitHub Copilot (Chat mode)** - scaffolding, code generation, documenting
- **ChatGPT / Claude** (optional, as the group prefers) - proofreading, email drafts

## Tasks AI assisted with

1. **Initial project scaffold** - directory layout, Python package
   structure, and the SQLAlchemy `Event` + `Registration` models (an
   earlier draft of the project used a low-code platform; the team
   pivoted to Flask early and the AI re-scaffolded around the new stack).
2. **Server-side CRUD functions** - first drafts of `create_registration`,
   `update_registration`, `cancel_registration`. Now live as Flask routes
   in `routes.py`.
3. **Template logic** - wire-up of form handlers and navigation between
   pages. Now Jinja2 templates in `event_registration/templates/`.
4. **CSS theme** - first draft of `static/css/styles.css`.
5. **Documentation** - README, this AI-use statement, and the short report
   outline.

## What the group accepted

- The overall folder structure (`event_registration/` package split into
  `models.py` + `routes.py` + `templates/` + `static/`).
- The soft-delete pattern for cancellation (status = `'cancelled'` instead
  of a hard delete, preserving the audit trail).
- The capacity + duplicate-email validation rules.

## What the group corrected or rejected

- **Public participant list (privacy fix)** - the AI's initial scaffold
  exposed the organiser-only participants page via a public "View
  participants" button on the home page and a top-nav link. The team
  identified this as a data-protection issue (attendee names, emails,
  phone numbers, and accessibility notes would be publicly scrapable)
  and corrected it by adding a shared-password gate (`event_registration/auth.py`
  + `/login` route) and removing the public links. (Landed in PR #1.)
- **Removal of the redundant clipboard button** - the AI scaffold added
  a "Copy event ref to clipboard" button on the home page. The team
  reviewed the brief, saw that only one JavaScript interaction is
  required and that the live character counter already satisfies it,
  and removed the clipboard button as over-extrapolation beyond scope.
  (Landed in PR #1.)
- **Validation rules** - the AI's first draft of `register()` did not
  catch duplicate emails or sold-out events; the team added those checks
  explicitly after writing test cases.

## What the group learned

- AI accelerates boilerplate (config files, CRUD fns, CSS) significantly.
- It does **not** replace domain-specific validation - those came from us
  knowing the business rules (capacity, no duplicate emails).
- It needs to be checked against the brief: the AI scaffold went beyond
  what was asked in two places (public participants list, redundant
  clipboard button), both of which were caught and corrected in code review.

## Responsibility

The group has read, tested, and validated every line of code in this repo.
The acceptance criteria in `docs/Short_Report.md` § "Testing evidence" were
checked by hand before submission.
