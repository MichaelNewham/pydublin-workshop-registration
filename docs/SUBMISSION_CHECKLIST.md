# Submission checklist (for Alessandro / Block D)

Run through this list **before** building the Moodle submission ZIP. The ZIP
should contain only what the brief asks for; internal team docs are
deliberately excluded.

## Files to EXCLUDE from the submission ZIP

These are tracked in git (the team needs them), but the tutor doesn't need
to see them in the marking bundle:

- `docs/COLLABORATOR_NOTES.md` - internal team onboarding (per-student)
- `docs/CI_SETUP.md` - internal CI ops guide
- `docs/SUBMISSION_CHECKLIST.md` - this file
- `.github/` - GitHub Actions config (mentioned in report; raw files not
  needed by the tutor)
- `.git/` - git's own metadata (huge, never include)
- `.venv/`, `venv/`, `__pycache__/` - environment + build caches
- `event_registration/app.db` or any `*.db` - the demo database
- `*.log`, `.env` - secrets / noise

## Files to INCLUDE (the actual deliverable)

These map 1:1 to the brief's deliverable list:

```
event_registration/        # the Flask app source
run.py, requirements.txt
render.yaml, Procfile, .env.example
README.md
AUTHORS.md
data/seed_events.csv
docs/Short_Report.pdf      # export from Short_Report.md + screenshots
docs/Short_Report.md       # source too, in case the tutor wants it
docs/AI_USE_STATEMENT.md
docs/Individual_Contribution.csv
docs/Video_Demo_script.md  # ...and the recorded MP4 alongside it
docs/screenshots/          # embedded in the report
```

## Build the ZIP

From inside the `Project/` folder:

```bash
zip -r submission.zip . \
    -x '.git/*' \
    -x '.github/*' \
    -x '.venv/*' 'venv/*' '__pycache__/*' \
    -x 'docs/COLLABORATOR_NOTES.md' \
    -x 'docs/CI_SETUP.md' \
    -x 'docs/SUBMISSION_CHECKLIST.md' \
    -x '*.db' '*.log' '.env'
```

Then sanity-check it only contains what you intend:

```bash
unzip -l submission.zip | less
```

You should see `event_registration/` files, `docs/Short_Report.*`,
`README.md`, etc. - and **no** `.git`, no `COLLABORATOR_NOTES.md`, no caches.

## Final pre-submission checklist

- [ ] CI is green on the latest `main` commit
- [ ] Live URL works in a private browser tab:
      https://pydublin-workshop-registration.onrender.com
- [ ] `README.md`'s live URL matches the actual deployment
- [ ] No `[TODO]` markers left in `docs/Short_Report.md`
- [ ] Screenshots embedded in `Short_Report.md` and the exported PDF
- [ ] `Short_Report.pdf` is <= 8 pages (excluding appendices)
- [ ] Demo video MP4 is <= 7 minutes and follows `Video_Demo_script.md`
- [ ] `Individual_Contribution.csv` sums to 100 %
- [ ] ZIP opens cleanly on a fresh machine (no broken paths)
- [ ] Moodle upload successful before the deadline
