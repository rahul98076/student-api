install:
	pip install -r requirements.txt

run:
	python run.py

setup:
	python -m venv venv

test:
	python -m pytest


IMAGE_NAME = student-api
VERSION ?= v1

docker-build:
	docker build -t $(IMAGE_NAME):$(VERSION) .

docker-run:
	docker run --rm -p 5000:5000 --env-file .env $(IMAGE_NAME):$(VERSION)