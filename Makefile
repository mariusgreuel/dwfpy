PYTHON ?= python

BLACK_OPTIONS = --line-length 100 --skip-string-normalization

.PHONY: all
all: format check

.PHONY: check
check: check-pylint check-mypy check-black

.PHONY: check-pylint
check-pylint:
	$(PYTHON) -m pylint src examples

.PHONY: check-mypy
check-mypy:
	$(PYTHON) -m mypy src examples

.PHONY: check-black
check-black:
	$(PYTHON) -m black --check $(BLACK_OPTIONS) src examples --exclude '/bindings\.py'

.PHONY: format
format:
	$(PYTHON) -m black $(BLACK_OPTIONS) src examples --exclude '/bindings\.py'

.PHONY: build
build:
	$(PYTHON) -m build

.PHONY: upload
upload:
	$(PYTHON) -m twine upload -u __token__ dist/*

.PHONY: docs
docs:
	$(MAKE) -C docs html
