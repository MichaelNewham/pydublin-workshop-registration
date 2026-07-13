"""
event_registration.config
=========================

Environment-driven config. Reads from env vars first (Render / production),
falls back to safe local defaults.

DATABASE_URL:
  * If set (e.g. a Neon / Supabase / Render Postgres connection string) the
    app uses Postgres and registrations PERSIST across redeploys.
  * If unset, the app falls back to a local SQLite file at
    event_registration/app.db for dev / marking.

IMPORTANT: Render's free web tier has an EPHEMERAL filesystem - any file you
write (including app.db) is wiped on every deploy / rebuild / sleep cycle.
For a live demo where registrations must survive, set DATABASE_URL to a
managed Postgres instance (Neon's free tier works well).
"""

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def _resolve_database_uri() -> str:
    """Pick the DB URI.

    Priority:
      1. $DATABASE_URL (Postgres on Render / Neon / Supabase) - PERSISTENT.
      2. Fall back to a local SQLite file for dev / marking.

    Handles two real-world gotchas:
      * Heroku / Render historically hand out URLs that start with
        `postgres://`, which SQLAlchemy 2.x rejects. Rewrite to
        `postgresql://` so the app boots without manual edits.
      * If the user pastes a `postgresql+psycopg://` URL we leave it alone.
    """
    uri = os.environ.get("DATABASE_URL")
    if uri:
        # Render / Heroku convention fixup (SQLAlchemy >=1.4 dropped `postgres://`)
        if uri.startswith("postgres://"):
            uri = "postgresql://" + uri[len("postgres://"):]
        return uri
    # Local dev fallback (file lives in the package dir; see .gitignore).
    return f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}"


class Config:
    # Flask
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-me")

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = _resolve_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Connection-pool hardening for managed Postgres (Neon / Supabase /
    # Render Postgres). These providers close idle connections aggressively
    # (Neon's free tier suspends compute after ~5 min of inactivity), which
    # shows up as `SSL SYSCALL error` / `server closed the connection`.
    #   * pool_pre_ping: liveness-check each pooled conn before handing it out
    #     so a dropped connection is replaced transparently.
    #   * pool_recycle: recycle conns before the provider's idle timeout fires.
    # SQLite ignores these (it has no real pool), so it's safe to set globally.
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True, "pool_recycle": 280}

    # App
    EVENT_TITLE = os.environ.get("EVENT_TITLE", "PyDublin Workshop 2026")
    DEBUG = os.environ.get("FLASK_DEBUG", "0") == "1"
