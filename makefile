SHELL := /bin/bash

.PHONY: help
help:
	@echo "Usage: make [target]"
	@echo "Targets:"
	@echo "  help - Show this help"
	@echo "  install - Install packages"
	@echo "  install_poetry - Install poetry"
	@echo "  create_poetry_environment - Create poetry environment"

.PHONY: install_poetry
install_poetry:
	@echo "Installing poetry (source: https://python-poetry.org/docs/)..."
	curl -sSL https://install.python-poetry.org | python3 -

.PHONY: install
install:
	@echo "Installing packages..."
	poetry install

.PHONY: create_poetry_environment
create_poetry_environment:
	@echo "Creating poetry environment..."
	poetry env use python3.12

# MISSING INSTALL node
# MISSING INSTALL npm
# MISSING INSTALL npx

#
# Day to day commands
#

.PHONY: generate_output_css
generate_output_css:
	@echo "Generating output.css..."
	npx tailwindcss -i ./static/src/input.css -o ./static/src/output.css --watch

.PHONY: test
test:
	@echo "Running tests..."
	poetry run pytest

.PHONY: make_migrations
make_migrations:
	@echo "Making migrations..."
	poetry run python manage.py makemigrations

.PHONY: migrate
migrate:
	@echo "Running migrations..."
	poetry run python manage.py migrate

.PHONY: django_runserver
django_runserver:
	@echo "Running Django server..."
	poetry run python manage.py runserver

.PHONY: livereload
livereload:
	@echo "Running livereload..."
	poetry run python manage.py livereload