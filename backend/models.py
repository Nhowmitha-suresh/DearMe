"""Compatibility shim for legacy backend imports.

The real SQLAlchemy models live under app.models.
"""

from app.models import *  # noqa: F401,F403
