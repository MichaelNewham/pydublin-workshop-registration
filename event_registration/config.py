"""
event_registration.config
=========================

Environment-driven config. Reads from env vars first (Render / production),
falls back to safe local defaults.

NOTE: SQLite is fine for marking + development. In a long-lived deploy the
DB is ephemeral (resets each deploy) which is actually a feature for a demo.
"""

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    # Flask
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-me")

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # App
    EVENT_TITLE = os.environ.get("EVENT_TITLE", "PyDublin Workshop 2026")
    DEBUG = os.environ.get("FLASK_DEBUG", "0") == "1"
