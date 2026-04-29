"""Contract tests — these run against the unmodified template AND any fork.

Strategy: the unmodified template skips the runner-specific test (since the
handler raises NotImplementedError) but still validates the SHAPE of /health
AND the structural integrity of pyproject + Dockerfile via the import chain.

After implementing your runner, REMOVE the skip and assert real shapes.
"""
import pytest
from pmscope.testing import (
    assert_health_response_shape,
    assert_watchlist_response_shape,
)


@pytest.mark.asyncio
async def test_health_shape(client):
    resp = await client.get("/health")
    assert resp.status_code == 200
    assert_health_response_shape(resp.json())


@pytest.mark.asyncio
async def test_watchlist_scan_shape(client):
    """The placeholder runner raises NotImplementedError — that's expected for
    the unmodified template. Once you implement runner.py, REMOVE this skip
    and assert the shape of a real response.
    """
    resp = await client.post(
        "/api/v1/watchlist/scan",
        json={"entity_type": "username", "entity_value": "x"},
    )
    # build_wrapper_app catches the runner exception and returns 500 + error JSON.
    if resp.status_code == 500 and "NotImplementedError" in resp.text:
        pytest.skip("template default — implement runner.py to enable shape check")
    assert resp.status_code == 200
    assert_watchlist_response_shape(resp.json())


def test_local_manifest_uses_placeholders():
    """Sanity check: unmodified template DOES contain placeholder markers.

    Forks should DELETE this test (or replace with `assert_module_manifest_valid(...)`)
    once they fill in pmscope-module.yaml.
    """
    with open("pmscope-module.yaml") as f:
        content = f.read()
    assert "<MODULE_NAME>" in content, (
        "If you've renamed your module, replace this test with:\n"
        "    import yaml\n"
        "    from pmscope.testing import assert_module_manifest_valid\n"
        "    assert_module_manifest_valid(yaml.safe_load(open('pmscope-module.yaml')))"
    )
