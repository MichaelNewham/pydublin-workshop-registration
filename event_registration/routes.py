"""
event_registration.routes
=========================

All HTTP routes. Implements every Option A functional requirement:

    GET  /                           event information page (public)
    GET  /register                   registration form (public)
    POST /register                   create registration  (with validation)
    GET  /registration/<id>          detail page for each registration (public;
                                     attendees see their own confirmation here)
    GET  /login                      shared-password organiser sign-in
    POST /login                      validate + set session flag
    GET  /logout                     clear session, return home
    GET  /participants               list (organiser-only)
    GET  /registration/<id>/edit     edit form (organiser-only)
    POST /registration/<id>/edit     save edits (organiser-only)
    POST /registration/<id>/cancel   cancel a registration (soft delete, organiser-only)
    POST /registration/<id>/restore  restore a cancelled registration (organiser-only)

Design: the server-side organiser tools are gated by `@login_required`,
which checks a shared-password session flag (see auth.py). This keeps
attendee contact details off the public internet while staying inside
the brief's scope (no per-user accounts).

Business rules in this module:
  -> capacity check (cannot overbook)
  -> duplicate email check (one registration per email per event)
  -> soft-delete for cancellation (preserves audit trail)
"""

from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, request, flash, abort, session

from .extensions import db
from .models import Event, Registration
from .auth import login_required, is_organiser, ORGANISER_PASSWORD, _safe_eq

bp = Blueprint("routes", __name__)


def _get_demo_event():
    """Return the seeded demo Event (single-event demo app)."""
    return Event.query.first()


# =============================================================================
# Public routes
# =============================================================================
@bp.route("/")
def home():
    """Event information page."""
    event = _get_demo_event()
    if event is None:
        return render_template("home.html", event=None)
    return render_template(
        "home.html",
        event=event,
        seats_taken=event.seats_taken(),
        seats_remaining=event.seats_remaining(),
    )


@bp.route("/register", methods=["GET", "POST"])
def register():
    """Registration form for attendees."""
    event = _get_demo_event()
    if event is None:
        flash("No event is configured yet.", "warning")
        return redirect(url_for("routes.home"))

    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        email = (request.form.get("email") or "").strip().lower()
        phone = (request.form.get("phone") or "").strip()
        company = (request.form.get("company") or "").strip()
        notes = (request.form.get("notes") or "").strip()

        # ---- server-side validation (the business rules) ----
        if not name:
            flash("Name is required.", "danger")
        elif "@" not in email:
            flash("A valid email is required.", "danger")
        elif event.seats_remaining() <= 0:
            flash("Sorry, this event is sold out.", "danger")
        elif (
            Registration.query.filter_by(
                event_id=event.id, email=email, status="registered"
            ).first()
            is not None
        ):
            flash("That email is already registered for this event.", "danger")
        else:
            reg = Registration(
                name=name,
                email=email,
                phone=phone,
                company=company,
                notes=notes,
                event_id=event.id,
            )
            db.session.add(reg)
            db.session.commit()
            flash(f"Registered successfully! Your ref is {reg.ref}.", "success")
            return redirect(url_for("routes.detail", reg_id=reg.id))

        # re-render with submitted values so the user doesn't lose typing
        return render_template(
            "register.html",
            event=event,
            form=request.form,
        )

    return render_template("register.html", event=event, form=None)


# =============================================================================
# Organiser auth (shared-password gate; see auth.py)
# =============================================================================
@bp.route("/login", methods=["GET", "POST"])
def login():
    """Shared-password organiser login."""
    if request.method == "POST":
        submitted = request.form.get("password", "")
        if _safe_eq(submitted, ORGANISER_PASSWORD):
            session["is_organiser"] = True
            flash("Signed in as organiser.", "success")
            next_url = session.pop("next_url", None) or url_for("routes.participants")
            return redirect(next_url)
        flash("Incorrect password.", "danger")
    return render_template("login.html")


@bp.route("/logout", methods=["POST"])
def logout():
    """Clear the organiser session flag."""
    session.pop("is_organiser", None)
    flash("Signed out.", "info")
    return redirect(url_for("routes.home"))


# =============================================================================
# Organiser routes (gated by @login_required)
# =============================================================================
@bp.route("/participants")
@login_required
def participants():
    """List of registered participants for the organiser."""
    event = _get_demo_event()
    registrations = (
        Registration.query.filter_by(status="registered")
        .order_by(Registration.created_at.desc())
        .all()
    )
    return render_template(
        "participants.html",
        event=event,
        registrations=registrations,
        count=len(registrations),
    )


@bp.route("/registration/<int:reg_id>")
def detail(reg_id):
    """Detail page for a single registration.

    Stays PUBLIC: attendees are redirected here after they register so they
    can see their own confirmation + ref. There is no per-attendee login.
    """
    reg = db.session.get(Registration, reg_id) or abort(404)
    return render_template("detail.html", reg=reg)


@bp.route("/registration/<int:reg_id>/edit", methods=["GET", "POST"])
@login_required
def edit(reg_id):
    """Edit an existing registration (organiser-only)."""
    reg = db.session.get(Registration, reg_id) or abort(404)

    if request.method == "POST":
        reg.name = (request.form.get("name") or "").strip()
        reg.email = (request.form.get("email") or "").strip().lower()
        reg.phone = (request.form.get("phone") or "").strip()
        reg.company = (request.form.get("company") or "").strip()
        reg.notes = (request.form.get("notes") or "").strip()
        db.session.commit()
        flash("Registration updated.", "success")
        return redirect(url_for("routes.detail", reg_id=reg.id))

    return render_template("edit.html", reg=reg)


@bp.route("/registration/<int:reg_id>/cancel", methods=["POST"])
@login_required
def cancel(reg_id):
    """Soft-delete: mark a Registration as 'cancelled' (organiser-only)."""
    reg = db.session.get(Registration, reg_id) or abort(404)
    reg.status = "cancelled"
    db.session.commit()
    flash("Registration cancelled.", "warning")
    return redirect(url_for("routes.detail", reg_id=reg.id))


@bp.route("/registration/<int:reg_id>/restore", methods=["POST"])
@login_required
def restore(reg_id):
    """Restore a previously cancelled registration (organiser-only)."""
    reg = db.session.get(Registration, reg_id) or abort(404)
    reg.status = "registered"
    db.session.commit()
    flash("Registration restored.", "success")
    return redirect(url_for("routes.detail", reg_id=reg.id))


# =============================================================================
# Error handlers
# =============================================================================
@bp.app_errorhandler(404)
def not_found(err):
    return render_template("error.html", code=404, message="Page not found"), 404


@bp.app_errorhandler(500)
def server_error(err):
    return render_template("error.html", code=500, message="Server error"), 500
