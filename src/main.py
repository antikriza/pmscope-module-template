"""Module entry point — wires runner.py into pmscope.build_wrapper_app.

TODO(rename): change `name=` and `description=` after fork.
"""
from pmscope import build_wrapper_app

from src.runner import watchlist_handler

app = build_wrapper_app(
    # TODO(rename): module slug (lowercase, hyphens) — match name in pmscope-module.yaml
    name="pmscope-mymodule",
    version="0.0.1",
    # TODO(describe): what this module does
    description="PM-SCOPE module template — fork and customize",
    # TODO(entity_types): pick the entity types your tool supports
    entity_types={"username"},
    redis_url=None,  # set if you need a job store; see lib/pmscope/redis_job_store.py
    watchlist_handler=watchlist_handler,
)
