# =============================================================================
# ServerModule1.py - server-side Python for the Event Registration app
# =============================================================================
# This module contains the @anvil.server.callable functions invoked from
# client_code/. All DB access is server-side for security (per Option B's
# governance talking point in the report). Client config in anvil.yaml sets
# table access to `client: full` for demo simplicity, but in a production
# build you would set `client: none` and route everything through here.
#
# Reference: https://anvil.works/docs/server
# =============================================================================

import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime


# -----------------------------------------------------------------------------
# Initialise the app with a seed Event row, if none exists yet.
# -----------------------------------------------------------------------------
# Called from HomeForm on first load. Idempotent - safe to call every startup.
@anvil.server.callable
def get_or_create_demo_event():
    """Return the default PyDublin Workshop event, creating it if needed."""
    event = app_tables.event.get(title="PyDublin Workshop 2026")
    if event is None:
        event = app_tables.event.add_row(
            title="PyDublin Workshop 2026",
            date=datetime(2026, 9, 15, 9, 30),
            location="Dublin Digital Hub, 10-12 Thomas St, Dublin 8",
            capacity=40,
            price=25.00,
            description=(
                "A one-day, hands-on workshop introducing Python for "
                "business automation: data cleaning with pandas, building "
                "Flask web apps, and scraping with BeautifulSoup. "
                "Laptops required. Coffee & lunch provided."
            ),
        )
    return event


# -----------------------------------------------------------------------------
# READ - public
# -----------------------------------------------------------------------------
@anvil.server.callable
def get_event():
    """Return the demo Event row (a dict-like app_tables row)."""
    return get_or_create_demo_event()


@anvil.server.callable
def count_registrations(event, status="registered"):
    """How many active registrations does this Event have?"""
    if event is None:
        return 0
    return len(
        app_tables.registration.search(event_id=event, status=status)
    )


@anvil.server.callable
def list_registrations(event=None, status="registered"):
    """Return all registrations, optionally filtered by event and/or status.

    Returns a list so the client can render it in a RepeatingPanel without
    further round-trips.
    """
    search_kwargs = {}
    if event is not None:
        search_kwargs["event_id"] = event
    if status is not None:
        search_kwargs["status"] = status
    # Newest first
    return list(
        app_tables.registration.search(
            tables.api.order_by("created_at", ascending=False), **search_kwargs
        )
    )


# -----------------------------------------------------------------------------
# CREATE - the registration form
# -----------------------------------------------------------------------------
@anvil.server.callable
def create_registration(name, email, phone, company, notes, event=None):
    """Create a new Registration row.

    Validates capacity and email uniqueness; raises ValueError on failure so
    the Form can display the message to the user.
    """
    if event is None:
        event = get_or_create_demo_event()

    name = (name or "").strip()
    email = (email or "").strip().lower()
    if not name:
        raise ValueError("Name is required.")
    if "@" not in email:
        raise ValueError("A valid email is required.")

    # Capacity check
    if count_registrations(event) >= (event["capacity"] or 0):
        raise ValueError("Sorry, this event is sold out.")

    # Duplicate-email check
    if app_tables.registration.get(email=email, event_id=event, status="registered"):
        raise ValueError("That email is already registered for this event.")

    row = app_tables.registration.add_row(
        name=name,
        email=email,
        phone=(phone or "").strip(),
        company=(company or "").strip(),
        notes=(notes or "").strip(),
        status="registered",
        created_at=datetime.now(),
        event_id=event,
    )
    return row


# -----------------------------------------------------------------------------
# READ one - the detail / edit forms
# -----------------------------------------------------------------------------
@anvil.server.callable
def get_registration(reg_id):
    """Fetch a single Registration row by its row id."""
    return app_tables.registration.get_by_id(reg_id)


# -----------------------------------------------------------------------------
# UPDATE - the edit form
# -----------------------------------------------------------------------------
@anvil.server.callable
def update_registration(reg_id, **fields):
    """Update editable fields on an existing Registration.

    Only the user-editable columns are accepted. Status changes go through
    cancel_registration() so the audit trail stays consistent.
    """
    row = app_tables.registration.get_by_id(reg_id)
    if row is None:
        raise ValueError("Registration not found.")

    allowed = {"name", "email", "phone", "company", "notes"}
    for key, value in fields.items():
        if key in allowed:
            row[key] = value
        # silently ignore unknown keys so we don't widen the surface
    return row


# -----------------------------------------------------------------------------
# DELETE / soft-delete - the "Cancel a registration" requirement
# -----------------------------------------------------------------------------
@anvil.server.callable
def cancel_registration(reg_id):
    """Soft-delete: mark a Registration as 'cancelled' rather than removing it.

    Soft-delete keeps the audit trail intact for the organiser's report -
    a deliberate design decision advocated in the project report.
    """
    row = app_tables.registration.get_by_id(reg_id)
    if row is None:
        raise ValueError("Registration not found.")
    row["status"] = "cancelled"
    return row


# -----------------------------------------------------------------------------
# RESTORE - undo an accidental cancel
# -----------------------------------------------------------------------------
@anvil.server.callable
def restore_registration(reg_id):
    """Re-activate a previously cancelled registration."""
    row = app_tables.registration.get_by_id(reg_id)
    if row is None:
        raise ValueError("Registration not found.")
    row["status"] = "registered"
    return row
