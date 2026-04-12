SHELL := /bin/bash
VENV ?= .venv
PY := python3
PIP := $(VENV)/bin/pip
PYTEST := $(VENV)/bin/pytest
FLAKE8 := $(VENV)/bin/flake8
.PHONY: help venv install lint test build run shell clean

help:
	@echo "Targets: install lint test build run shell clean"

venv:
	$(PY) -m venv $(VENV)
	$(PIP) install --upgrade pip

install: venv
	$(PIP) install -r requirements.txt

lint:
	$(FLAKE8) .

test:
	$(PYTEST)

build:
	docker build -t leaffliction-dev .

run:
	docker run --rm -it -v "$(PWD)":/app leaffliction-dev

shell:
	@echo "Activate venv: source $(VENV)/bin/activate"

clean:
	rm -rf $(VENV) __pycache__ *.pyc
