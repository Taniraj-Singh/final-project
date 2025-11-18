.PHONY: help build up down logs shell test clean migrate

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

build: ## Build the Docker images
	docker-compose build

up: ## Start all services
	docker-compose up -d

down: ## Stop all services
	docker-compose down

logs: ## Show logs for all services
	docker-compose logs -f

logs-app: ## Show logs for the app service
	docker-compose logs -f app

logs-db: ## Show logs for the database service
	docker-compose logs -f db

shell: ## Open a shell in the app container
	docker-compose exec app bash

shell-db: ## Open a shell in the database container
	docker-compose exec db psql -U postgres -d predictive_maintenance

migrate: ## Run database migrations
	docker-compose exec app alembic upgrade head

migrate-create: ## Create a new migration (usage: make migrate-create MESSAGE="description")
	docker-compose exec app alembic revision --autogenerate -m "$(MESSAGE)"

test: ## Run tests
	docker-compose exec app python -m pytest

clean: ## Clean up containers and volumes
	docker-compose down -v
	docker system prune -f

dev: ## Start development environment
	docker-compose up -d db
	sleep 10
	alembic upgrade head
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

install: ## Install dependencies locally
	pip install -r requirements.txt

lint: ## Run linting
	docker-compose exec app python -m flake8 app/
	docker-compose exec app python -m black --check app/

format: ## Format code
	docker-compose exec app python -m black app/






