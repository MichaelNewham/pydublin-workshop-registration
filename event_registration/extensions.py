"""
event_registration.extensions
=============================

Flask extensions live here so we avoid circular imports between
__init__.py (create_app), models.py, and routes.py.
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
