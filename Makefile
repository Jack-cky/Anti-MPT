.PHONY: help build push pull dashboard pipeline down

COMPOSE_FILE := apps/compose.yaml
COMPOSE := docker compose -f $(COMPOSE_FILE)

help:
	@echo "Available targets:"
	@echo "  make help       # Show available targets"
	@echo "  make build      # Build the dashboard and pipeline container images"
	@echo "  make push       # Push the dashboard and pipeline container images to Docker Hub"
	@echo "  make pull       # Pull the pipeline container image from Docker Hub"
	@echo "  make dashboard  # Start the dashboard service in detached mode"
	@echo "  make pipeline   # Run the pipeline service using the existing image"
	@echo "  make down       # Stop and remove services defined in apps/compose.yaml"

build:
	$(COMPOSE) build

push:
	$(COMPOSE) push

pull:
	$(COMPOSE) pull pipeline

dashboard:
	$(COMPOSE) up -d --no-build dashboard

pipeline:
	$(COMPOSE) run --rm --pull never pipeline

down:
	$(COMPOSE) down
