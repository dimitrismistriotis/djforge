SHELL := /bin/bash

.PHONY: help
help:
	@echo "Usage: make [target]"
	@echo "Targets:"
	@echo "  help - Show this help"
	@echo "  install - Install packages"
	@echo "  create_poetry_environment - Create poetry environment"

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

.PHONY: django_runserver
django_runserver:
	@echo "Running Django server..."
	poetry run python manage.py runserver
