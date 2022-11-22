
install:
	python -m pip install -r requirements.txt

install-dev:
	python -m pip install -r requirements-dev.txt

compile:
	pip-compile requirements.in
	pip-compile requirements-dev.in

lint:
	python -m flake8
	python -m mypy

format-check:
	python -m black --diff --check .
	python -m isort -c .
