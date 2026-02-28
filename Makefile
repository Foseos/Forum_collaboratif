.PHONY: help install migrate run test lint format createsuperuser shell docker-up docker-down

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install backend dependencies
	cd backend && pip install -r requirements/dev.txt

migrate: ## Run database migrations
	cd backend && python manage.py makemigrations && python manage.py migrate

run: ## Run development server
	cd backend && python manage.py runserver

test: ## Run tests
	cd backend && python manage.py test --verbosity=2

lint: ## Run linters
	cd backend && flake8 .

format: ## Format code with black
	cd backend && black .

createsuperuser: ## Create a superuser
	cd backend && python manage.py createsuperuser

shell: ## Open Django shell
	cd backend && python manage.py shell

docker-up: ## Start all services with Docker
	docker-compose up -d --build

docker-down: ## Stop all Docker services
	docker-compose down

docker-logs: ## View Docker logs
	docker-compose logs -f
