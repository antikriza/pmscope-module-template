# PM-SCOPE Module Template

Fork this template to scaffold a new OSINT module for PM-SCOPE.

## What you get

- Working `build_wrapper_app()` skeleton
- Contract-tested `/health` + `/api/v1/watchlist/scan` endpoints
- Dockerfile + GitHub Actions for tag-triggered GHCR push
- Makefile (`make dev`, `make test`, `make image`)

## Step 1: Use this template

Click "Use this template" on GitHub. Choose `<your-name>/pmscope-<tool>` as the new repo name.

## Step 2: Fork prerequisites

1. Clone PM-SCOPE alongside your new module: `git clone https://github.com/antikriza/PM-SCOPE.git ../PM-SCOPE`
2. `cd ../PM-SCOPE && cp .env.example .env` (set `INTERNAL_SERVICE_TOKEN`)

## Step 3: Rename

Run a global search-replace:

- `pmscope-mymodule` → `pmscope-<your-tool>`
- `<MODULE_NAME>`, `<DISPLAY_NAME>`, etc. in `pmscope-module.yaml` → real values

Update:

- `pyproject.toml` — name, description, dependencies
- `src/main.py` — name, description, entity_types
- `pmscope-module.yaml` — every TODO marker
- `docker-compose.override.yml` — service name + Redis DB number
- `.github/workflows/release.yml` — image name

## Step 4: Implement the runner

Open `src/runner.py`. Replace the `NotImplementedError` body with your tool's logic.
The function MUST return:

```python
{
    "entities": [{...}],
    "attributes": {...},
    "mentions": [...],
    "metadata": {"scan_id": "...", "timestamp": "...", "source_tool": "..."}
}
```

## Step 5: Test locally

```
make test
make dev
# In another shell: curl http://localhost:8000/health
```

### docker-compose project name

This template assumes `COMPOSE_PROJECT_NAME=pmscope` (the Makefile sets this by default).
If you've already started PM-SCOPE under a different project name, the override file's
`pmscope_pmscope-internal` network won't exist and `make dev` will fail with
`network <name> not found`.

Workarounds (any one):

- Run `make dev COMPOSE_PROJECT_NAME=<your-name>` AND edit `docker-compose.override.yml`
  to reference `<your-name>_pmscope-internal`.
- Restart your PM-SCOPE checkout with `COMPOSE_PROJECT_NAME=pmscope` set.
- Dynamically discover the network name:
  `docker network ls --filter name=pmscope-internal -q | head -1`

## Step 6: Ship the image

1. Commit + tag:

   ```
   git tag v0.1.0 && git push origin v0.1.0
   ```

2. GitHub Actions builds the image and prints the digest in the workflow notice.
3. Make the GHCR package public (Settings → Packages → your module → Change visibility).

## Step 7: PR the manifest into PM-SCOPE

In the PM-SCOPE repo, create `services/api/src/registry/modules.d/<your-tool>.yaml`:

```yaml
manifest_version: 1
name: pmscope-<your-tool>
display_name: "<Your Tool>"
version: 0.1.0
docker_image: "ghcr.io/<owner>/pmscope-<your-tool>@sha256:<digest>"
sdk_version: ">=0.1,<0.2"
entity_types: [...]
watchlist_severity: medium
chat_command: /<your-tool>
chat_usage: "/<your-tool> <target>"
chat_description: "..."
```

Open a PR. After merge, restart the API container — your module appears in `/admin/health` and chat commands.

## Step 8: Done

See `docs/MODULE-DEVELOPMENT.md` in PM-SCOPE for the full reference, gotchas, and Phase 6+ enhancements.

---

## Vendored wheel — temporary workaround until pypiserver lands

PM-SCOPE is a **private GitHub repo**, so external module repos cannot install
`pmscope-sdk` via `pip install git+https://github.com/<owner>/PM-SCOPE.git#subdirectory=lib`
— GitHub Actions runners (and most fork environments) lack credentials to read the
private repo and the install fails with `fatal: could not read Username for
'https://github.com'`.

**Workaround (this template uses it):** ship the `pmscope-sdk` wheel inside the
template under `wheels/pmscope_sdk-0.1.0-py3-none-any.whl`. The `Dockerfile`,
`.github/workflows/ci.yml`, and the `Makefile`'s `test` target install the wheel
first, then the module with `--no-deps`. This keeps forks working with zero
authentication setup.

**To refresh the wheel when bumping `pmscope-sdk`:**

```bash
# In your PM-SCOPE checkout
cd /path/to/PM-SCOPE/lib
python3 -m pip install build  # one-time
python3 -m build --wheel --outdir /path/to/your-module/wheels/

# Then commit the new wheel + bump pmscope-sdk version pin in pyproject.toml
```

**Permanent fix (planned):** PM-SCOPE Phase 5 PLAN 06 deploys a self-hosted
`pypiserver` at `pypi.<DOMAIN>` so modules can `pip install pmscope-sdk` like
any normal PyPI package. Once that lands, this section will be deleted and
`wheels/` removed.
