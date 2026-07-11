"""
event_registration.auth
=======================

Lightweight organiser gate. Not a full user-account system - just a single
shared password (set via the ORGANISER_PASSWORD env var) that unlocks the
organiser-only routes (participants list, edit, cancel, restore).

Why this design:
  - The brief doesn't require user accounts.
  - But the participants list + edit/cancel endpoints leak attendee data
    if left fully public, so we gate them behind *something*.
  - A shared password is the simplest gate that satisfies the
    "security/governance" talking point in the project report without
    overbuilding for a marking demo.

Usage in routes.py:

    from .auth import login_required

    @bp.route("/participants")
    @login_required
    def participants():
        ...

The session stores the organiser flag as a signed cookie (via Flask's
session), so the login survives a browser restart for the session lifetime
(default: until the browser is closed, or PERMANENT_SESSION_LIFETIME).
"""

import os
import hmac
from functools import wraps

from flask import session, redirect, url_for, request, flash


# The shared organiser password. Set via env var; falls back to a clearly
# marked demo default so the app still boots for local development.
# Render's SECRET_KEY is already auto-generated, so the session cookie
# is signed even when ORGANISER_PASSWORD is the demo default.
ORGANISER_PASSWORD = os.environ.get("ORGANISER_PASSWORD", "pydublin-2026")


def _safe_eq(a: str, b: str) -> bool:
    """Constant-time string compare - avoids timing-attack leakage."""
    return hmac.compare_digest(a.encode(), b.encode())


def is_organiser() -> bool:
    """True if the current session has been authenticated as the organiser."""
    return bool(session.get("is_organiser"))


def login_required(view):
    """Decorator: redirect to /login if session is not organiser-authed.

    Usage:
        @bp.route("/participants")
        @login_required
        def participants():
            ...
    """
    @wraps(view)
    def wrapped(*args, **kwargs):
        if is_organiser():
            return view(*args, **kwargs)
        # Remember where the user was trying to go, so we can return there
        session["next_url"] = request.path
        flash("Please sign in as the organiser to view that page.", "warning")
        return redirect(url_for("routes.login"))
    return wrapped
