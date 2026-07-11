# CI setup (one-time manual step)

A GitHub Actions workflow file is checked into `.github/workflows/ci.yml`.
It runs on every push and pull request, and:

1. Installs dependencies from `requirements.txt`.
2. Compile-checks every `.py` file (`python -m compileall`).
3. Runs flake8 for serious issues (E9, F63, F7, F82).
4. Boots the Flask app via its `create_app()` factory and smoke-tests
   the `/`, `/register`, and `/participants` routes.

## Why isn't it already running?

The deploy token used by `git push` did not have the GitHub `workflow`
scope, which GitHub requires for any commit that touches files under
`.github/workflows/`. So the file lives in the repo but is awaiting
this one-time permission grant.

## To enable (takes ~30 seconds)

Choose ONE of the following:

### Option A - bump the deploy token scope (recommended)

```bash
gh auth refresh -h github.com -s workflow
git add .github/workflows/ci.yml
git commit -m "ci: enable GitHub Actions workflow"
git push origin main
```

After this, every future push and PR will trigger the CI run on GitHub.

### Option B - paste the file via the web UI

1. Open https://github.com/MichaelNewham/pydublin-workshop-registration
2. Click **Add file -> Create new file**.
3. Name it `.github/workflows/ci.yml`.
4. Paste the contents from your local copy at
   `.github/workflows/ci.yml`.
5. **Commit changes**.

The web UI uses your interactive browser session, so it doesn't need
the `workflow` scope on a token. The workflow starts running immediately
on the next push.

### Verify CI is running

After either option:

- Visit the **Actions** tab of the repo on GitHub.
- You should see a green tick (or yellow in-progress) next to the latest
  commit on `main`.
