"""Env-driven settings (Pydantic Settings recommended for v2 modules)."""
import os

INTERNAL_SERVICE_TOKEN = os.getenv("INTERNAL_SERVICE_TOKEN", "")

# TODO(env): declare any tool-specific env vars here, e.g.
# MYTOOL_API_KEY = os.getenv("MYTOOL_API_KEY", "")
