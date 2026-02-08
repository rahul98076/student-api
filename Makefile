PYTHON_CMD ?= python3
ifeq ($(OS),Windows_NT)
    PYTHON_CMD = python
endif

IMAGE_NAME = rahul98076/student-api
GIT_COMMIT := $(shell git rev-parse --short HEAD)
VERSION ?= $(if $(GIT_COMMIT),$(GIT_COMMIT),latest)

check-tools:
	@chmod +x scripts/setup.sh
	@./scripts/setup.sh

venv:
	$(PYTHON_CMD) -m venv venv

install:
	pip install -r requirements.txt

setup: check-tools venv install


run:
	$(PYTHON_CMD) run.py

test:
	$(PYTHON_CMD) -m pytest


up:
	docker compose up --build -d

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


lint:
	flake8 app/ run.py

build:
	docker build -t $(IMAGE_NAME):$(VERSION) .

push:
	docker push $(IMAGE_NAME):$(VERSION)


deploy: down up
	@echo "Deployment complete. Nginx is listening on port 8080."
