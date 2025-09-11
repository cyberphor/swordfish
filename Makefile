# ---------------------------------------------------------
# Set the default target.
# ---------------------------------------------------------

.DEFAULT_GOAL := build

# ---------------------------------------------------------
# Load environment variables.
# ---------------------------------------------------------

.PHONY: print-dot-env-files-used
.SILENT: print-dot-env-files-used

# Set the "env" to local if an argument is not provided.
ENV ?= local

# Set the "profile" to "core if an argument is not provided.
PROFILE ?= all

# Load the specified environment file.
ENV_FILE := .env.$(ENV)
include $(ENV_FILE)

print-dot-env-files-used:
	@echo "[+] Set environment variables using $(ENV_FILE)"

# ---------------------------------------------------------
# Build all the containers.
# ---------------------------------------------------------

.PHONY: build
.SILENT: build

build: print-dot-env-files-used
	docker compose --env-file $(ENV_FILE) --profile $(PROFILE) build 

# ---------------------------------------------------------
# Start all the containers.
# ---------------------------------------------------------

.PHONY: start
.SILENT: start

start: print-dot-env-files-used
	docker compose --env-file $(ENV_FILE) --profile $(PROFILE) up -d

# ---------------------------------------------------------
# Stop all the containers.
# ---------------------------------------------------------

.PHONY: stop
.SILENT: stop

stop: print-dot-env-files-used
	docker compose --env-file $(ENV_FILE) --profile $(PROFILE) down
