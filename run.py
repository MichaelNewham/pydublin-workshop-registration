"""
run.py - entry point for development.

    python run.py

Production: Render runs `gunicorn run:app` (the module-level `app`
instance defined below). See render.yaml + Procfile.
"""

import os
from event_registration import create_app

app = create_app()

if __name__ == "__main__":
    # Render sets PORT; locally default to Flask's 5000.
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=app.config.get("DEBUG", False))
