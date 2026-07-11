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
    """Seed the demo Event + a couple of sample registrations if DB is empty."""
    with app.app_context():
        if Event.query.first() is not None:
            return  # already seeded

        event = Event(
            title="PyDublin Workshop 2026 - Python for Business",
            date=datetime(2026, 9, 15, 9, 30),
            location="Dublin Digital Hub, 10-12 Thomas St, Dublin 8",
            capacity=40,
            price=25.00,
            description=(
                "A one-day, hands-on workshop introducing Python for "
                "business automation: data cleaning with pandas, building "
                "Flask web apps, and web scraping with BeautifulSoup. "
                "Laptops required. Coffee & lunch provided."
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
