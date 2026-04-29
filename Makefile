.PHONY: dev test build image lint
# PM-SCOPE checkout is expected at ../PM-SCOPE relative to this repo.
# Override with `make dev PMSCOPE_DIR=/path/to/PM-SCOPE`.
PMSCOPE_DIR ?= ../PM-SCOPE

# docker-compose project name. The `docker-compose.override.yml` references the
# network `pmscope_pmscope-internal`; that exact name only exists when compose is
# invoked with COMPOSE_PROJECT_NAME=pmscope. Override at the CLI if you have a
# PM-SCOPE checkout running under a different project name (`make dev COMPOSE_PROJECT_NAME=...`).
export COMPOSE_PROJECT_NAME ?= pmscope

dev:
	@test -d "$(PMSCOPE_DIR)" || (echo "ERROR: PM-SCOPE checkout not found at $(PMSCOPE_DIR). Set PMSCOPE_DIR or clone PM-SCOPE alongside this repo." && exit 1)
	@echo "Using COMPOSE_PROJECT_NAME=$(COMPOSE_PROJECT_NAME) — docker-compose.override.yml's pmscope_pmscope-internal network depends on this."
	docker compose -f $(PMSCOPE_DIR)/docker-compose.yml -f docker-compose.override.yml --profile app up --build

test:
	pip install ./wheels/pmscope_sdk-0.1.0-py3-none-any.whl
	pip install --no-deps -e .
	pip install pytest~=7.4.4 pytest-asyncio~=0.23.3 httpx~=0.26.0
	pytest tests/ -v

build:
	docker build -t pmscope-mymodule:dev .

image:
	@if [ -z "$(VERSION)" ]; then echo "Usage: make image VERSION=0.1.0 GH_OWNER=yourname"; exit 1; fi
	@if [ -z "$(GH_OWNER)" ]; then echo "Usage: make image VERSION=0.1.0 GH_OWNER=yourname"; exit 1; fi
	docker build -t ghcr.io/$(GH_OWNER)/pmscope-mymodule:$(VERSION) .
	docker push ghcr.io/$(GH_OWNER)/pmscope-mymodule:$(VERSION)
	@docker inspect ghcr.io/$(GH_OWNER)/pmscope-mymodule:$(VERSION) | jq -r '.[0].RepoDigests[0]'

lint:
	pip install ruff && ruff check src/ tests/
