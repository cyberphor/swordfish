# ---------------------------------------------------------
# Load the specified environment variables file.
# ---------------------------------------------------------

.DEFAULT_GOAL := build
COMPOSE_BAKE := true
ENV_FILE ?= .env
include $(ENV_FILE)

# Set the Docker Compose profile to "all" if an argument is not provided.
DOCKER_COMPOSE_PROFILE ?= all

# ---------------------------------------------------------
# Build the containers.
# ---------------------------------------------------------

.PHONY: build
.SILENT: build

build: 
	docker compose --profile $(DOCKER_COMPOSE_PROFILE) --env-file $(ENV_FILE) build --no-cache 

# ---------------------------------------------------------
# Start the containers.
# ---------------------------------------------------------

.PHONY: start
.SILENT: start

start:
	docker compose --profile $(DOCKER_COMPOSE_PROFILE) --env-file $(ENV_FILE) up -d

# ---------------------------------------------------------
# Verify the eMASS API server works.
# ---------------------------------------------------------

.PHONY: verify
.SILENT: verify

verify: 
	curl -X POST http://localhost:4010/api/api-key -H "user-uid: ${EMASS_USER_UID}" -H "api-key: ${EMASS_API_KEY}" &&\
	echo ""

# ---------------------------------------------------------
# Stop the containers.
# ---------------------------------------------------------

.PHONY: stop
.SILENT: stop

stop: 
	docker compose --profile $(DOCKER_COMPOSE_PROFILE) --env-file $(ENV_FILE) down

# ---------------------------------------------------------
# Build and serve the docs.
# ---------------------------------------------------------

.PHONY: docs
.SILENT: docs

docs: 
	uv run mkdocs serve --dev-addr=0.0.0.0:5050
