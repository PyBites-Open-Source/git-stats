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

.PHONY: unit
unit:
	pytest tests/unit

.PHONY: functional
functional:
	pytest tests/functional

.PHONY: test
test: unit

.PHONY: testall
testall: unit functional

.PHONY: coverage
coverage:
	pytest --cov=stats --cov-report term-missing

.PHONY: ci
ci: lint typing test
