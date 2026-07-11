# CI setup

**Status: live.** The GitHub Actions workflow in `.github/workflows/ci.yml`
is running on every push and PR to `main`. First passing run: commit
`d6eaa3f`, 16 seconds, July 11 2026.

Run history: https://github.com/MichaelNewham/pydublin-workshop-registration/actions

## What the workflow does

On every push to `main` and every PR targeting `main`, GitHub provisions a
fresh Ubuntu + Python 3.11 runner and:

1. Installs dependencies from `requirements.txt`.
2. Compile-checks every `.py` file (`python -m compileall`).
3. Runs `flake8 --select=E9,F63,F7,F82` (catches the serious stuff only:
   syntax errors, undefined names, starred-assignment bugs).
4. Boots the app via its `create_app()` factory and smoke-tests the
   `/`, `/register`, and `/participants` routes with a Flask test client,
   asserting each returns 200.

The whole job finishes in ~15-20 seconds.

## Prerequisites (already satisfied on this repo)

- `.github/workflows/ci.yml` must be committed to the default branch.
- The token used to push it needs the GitHub `workflow` scope. We added
  this scope to the `MichaelNewham` GitHub account's stored credentials
  via `gh auth refresh -h github.com -s workflow`.

## Running the workflow locally

Before pushing, you can run the same checks by hand:

```bash
pip install -r requirements.txt flake8
python -m compileall event_registration run.py
flake8 event_registration run.py --max-line-length=100 --select=E9,F63,F7,F82
python -c "from event_registration import create_app; \
  app = create_app(); \
  c = app.test_client(); \
  assert c.get('/').status_code == 200; \
  assert c.get('/register').status_code == 200; \
  assert c.get('/participants').status_code == 200; \
  print('OK')"
```

If all three pass locally, CI will almost certainly pass too.

## If CI fails on a push

Click the red ❌ next to the commit on GitHub, then click the failed step
for full logs. The most common causes are:

- A syntax error slipped in (the `compileall` step will catch it).
- A typo'd route name caused a 500 on `/`, `/register`, or `/participants`.
- An import error (e.g. circular import) - flake8 will report `F401` / `F811`.
