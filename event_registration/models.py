"""
event_registration.models
=========================

Two SQLAlchemy models with a one-to-many relationship:
    Event (1) < (N) Registration

Satisfies the Option A requirement: "at least two related tables".
"""

from datetime import datetime
from .extensions import db


class Event(db.Model):
    __tablename__ = "event"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, nullable=True)
    location = db.Column(db.String(300), nullable=True)
    capacity = db.Column(db.Integer, nullable=False, default=40)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False, default=0.0)

    # Relationship: one Event → many Registrations.
    # cascade signals: cancelling an Event cancels its Registrations.
    registrations = db.relationship(
        "Registration",
        backref="event",
        cascade="all, delete-orphan",
        lazy="dynamic",
    )

    def seats_taken(self):
        """Active (non-cancelled) registrations only."""
        return self.registrations.filter_by(status="registered").count()

    def seats_remaining(self):
        return max(0, (self.capacity or 0) - self.seats_taken())

    def __repr__(self):
        return f"<Event {self.id} {self.title!r}>"


class Registration(db.Model):
    __tablename__ = "registration"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, index=True)
    phone = db.Column(db.String(50), nullable=True)
    company = db.Column(db.String(200), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), nullable=False, default="registered")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign key - the relationship that satisfies ">=2 related tables"
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"), nullable=False)

    @property
    def ref(self):
        """Short human-readable reference, used in the UI + clipboard JS."""
        return f"PYDUB-2026-{self.id:04d}"

    def __repr__(self):
        return f"<Registration {self.id} {self.email!r}>"
