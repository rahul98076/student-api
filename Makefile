IMAGE_NAME = student-api
VERSION ?= v1

check-tools:
	@chmod +x scripts/setup.sh
	@./scripts/setup.sh

venv:
	python -m venv venv

install:
	pip install -r requirements.txt

setup: check-tools venv install


run:
	python run.py

test:
	python -m pytest


up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

migrate:
	docker compose exec api flask db upgrade

clean-docker:
	docker compose down -v


start:
	docker compose up -d --wait
	docker compose exec api flask db upgrade
	@echo "-----------------------------------"
	@echo "Student API is running on http://localhost:5000"
	@echo "-----------------------------------"