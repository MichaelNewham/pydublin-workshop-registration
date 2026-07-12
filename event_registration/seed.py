"""
event_registration.seed
======================

On first boot the DB is empty. This module seeds a demo Event so the app
has something to show on the homepage immediately. Idempotent.

Replaces the old Anvil `get_or_create_demo_event()` server function.
"""

from datetime import datetime
from .extensions import db
from .models import Event, Registration


def seed_demo_data(app):
    """Seed or update the demo Event + a couple of sample registrations.

    Idempotent on first boot (creates everything). On subsequent boots the
    Event row is UPDATED to match this function - so when the team rebrands
    (e.g. Michael's PyCon Ireland 2026 change), the new title / date / location
    / description propagate to existing databases without manual cleanup.

    Two sample Registrations are added only on first boot (not re-added later).
    """
    with app.app_context():
        event = Event.query.first()

        if event is None:
            # First boot: create everything.
            event = Event(
                title="PyCon Ireland 2026 - Python for Business",
                date=datetime(2026, 10, 17, 9, 30),
                location="Trinity College Dublin, College Green, Dublin 2",
                capacity=40,
                price=25.00,
                description=(
                    "A one-day, single-track conference day introducing Python "
                    "for business automation: data cleaning with pandas, building "
                    "Flask web apps, and web scraping with BeautifulSoup. "
                    "Anchored to the real PyCon Ireland 2026 announcement "
                    "(python.ie). Laptops required. Coffee & lunch provided."
                ),
            )
            db.session.add(event)
            db.session.flush()  # get an id without full commit

            # Two sample registrations so the participants list isn't empty
            sample = [
                Registration(
                    name="Alice Demo",
                    email="alice@example.com",
                    phone="+353 86 100 2000",
                    company="Demo Co.",
                    notes="Vegetarian meal",
                    event_id=event.id,
                ),
                Registration(
                    name="Bob Example",
                    email="bob@example.com",
                    phone="+353 87 300 4000",
                    company="Example Ltd.",
                    notes="",
                    event_id=event.id,
                ),
            ]
            db.session.add_all(sample)
            db.session.commit()

        else:
            # Subsequent boot: update the in-place Event row to match this
            # function. Lets the team re-theme without manual DB cleanup.
            # (Registrations are left untouched.)
            event.title = "PyCon Ireland 2026 - Python for Business"
            event.date = datetime(2026, 10, 17, 9, 30)
            event.location = "Trinity College Dublin, College Green, Dublin 2"
            event.description = (
                "A one-day, single-track conference day introducing Python "
                "for business automation: data cleaning with pandas, building "
                "Flask web apps, and web scraping with BeautifulSoup. "
                "Anchored to the real PyCon Ireland 2026 announcement "
                "(python.ie). Laptops required. Coffee & lunch provided."
            )
            # capacity + price intentionally not overwritten - we don't want a
            # code change here to clobber values the organiser may have set
            # manually via a future admin UI.
            db.session.commit()