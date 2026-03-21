# ---------------------------------------------------------
# Misc.
# ---------------------------------------------------------

# Set the default goal.
.DEFAULT_GOAL := build

# Tell Docker to build images in parallel.
COMPOSE_BAKE := true

# Set the environment variables file to ".env" if an argument is not provided.
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
# Stop the containers.
# ---------------------------------------------------------

.PHONY: stop
.SILENT: stop

stop: 
	docker compose --profile $(DOCKER_COMPOSE_PROFILE) --env-file $(ENV_FILE) down
