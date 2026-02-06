install:
	pip install -r requirements.txt

run:
	python run.py

setup:
	python -m venv venv

test:
	python -m pytest