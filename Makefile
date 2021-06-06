.PHONY: venv
venv:
	python3.9 -m venv venv

.PHONY: install
install:
	pip install -r requirements/dev.txt

.PHONY: lint
lint:
	flake8 stats tests

.PHONY: typing
typing:
	mypy stats tests

.PHONY: test
test:
	pytest

.PHONY: coverage
coverage:
	pytest --cov=stats --cov-report term-missing

.PHONY: ci
ci: lint typing test
