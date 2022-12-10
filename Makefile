
install:
	python -m pip install -r requirements.txt

install-dev:
	python -m pip install -r requirements-dev.txt

compile:
	pip-compile pyproject.toml
	pip-compile --extra=dev --output-file=requirements-dev.txt pyproject.toml

lint:
	python -m flake8
	python -m mypy

format-check:
	python -m black --diff --check .
	python -m isort -c .
