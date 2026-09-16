.PHONY: help build push pull up down

COMPOSE_FILE := hscs/compose.yaml
COMPOSE := docker compose -f $(COMPOSE_FILE)

help:
	@echo "Available targets:"
	@echo "  make help       # Show available targets"
	@echo "  make build      # Build the api and web container images"
	@echo "  make push       # Push the api and web container images to Docker Hub"
	@echo "  make pull       # Pull the api and web container images from Docker Hub"
	@echo "  make up         # Start the api and web services in detached mode"
	@echo "  make down       # Stop and remove services defined in hscs/compose.yaml"

build:
	$(COMPOSE) build

push:
	$(COMPOSE) push

pull:
	$(COMPOSE) pull

up:
	$(COMPOSE) up -d --no-build

down:
	$(COMPOSE) down
