"""Tool-specific runner — implement watchlist_handler.

The handler MUST return a dict matching the canonical watchlist scan shape:

    {
        "entities":   [{...}],
        "attributes": {...},
        "mentions":   [{...}],
        "metadata":   {"scan_id": str, "timestamp": ISO, "source_tool": str},
    }

Use pmscope.testing.assert_watchlist_response_shape() in your tests.
"""
from datetime import datetime, timezone


async def watchlist_handler(entity_type: str, entity_value: str) -> dict:
    # TODO(implement): query your OSINT tool here.
    # Replace this NotImplementedError with real logic. The contract test in
    # tests/test_contract.py SKIPS while NotImplementedError is raised, so the
    # unmodified template stays green — once you implement, delete the skip.
    raise NotImplementedError(
        "watchlist_handler is the entry point your tool calls. "
        "See README.md 'Step 4: Implement the runner' for the contract."
    )
