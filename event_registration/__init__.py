"""
event_registration
==================

Flask app factory. Usage:

    from event_registration import create_app
    app = create_app()
    app.run(debug=True)

The `run.py` at the project root is the CLI entry point that does this.
"""

import os
from flask import Flask

from .config import Config
from .extensions import db
from .models import Event, Registration  # noqa: F401  (ensures models register)
from .seed import seed_demo_data


def create_app(config_class=Config):
    """Application factory pattern. See Flask docs."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Init extensions
    db.init_app(app)

    # Register the blueprint (all routes)
    from .routes import bp
    app.register_blueprint(bp)

    # Build the DB schema + seed on first boot. Safe because create_all is
    # idempotent and seed_demo_data checks for an existing Event.
    with app.app_context():
        db.create_all()
        seed_demo_data(app)

    @app.context_processor
    def inject_globals():
        """Make the site title + organiser flag available in every template."""
        from .auth import is_organiser  # local import to avoid circular at boot
        event = Event.query.first()
        return {
            "site_title": (event.title if event else "Event Registration"),
            "is_organiser": is_organiser(),
        }

    return app
