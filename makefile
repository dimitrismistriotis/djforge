SHELL := /bin/bash

.SILENT: help

.PHONY: default
default: help

# The following fgrep will dynamically print all targets
# that have a comment beginning with '##' including help.
.PHONY: help
help:				## Show help message.
	echo "Usage: make [target]"
	echo "Targets:"
	fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

.PHONY: install_poetry
install_poetry:
	@echo "Installing poetry (source: https://python-poetry.org/docs/)..."
	curl -sSL https://install.python-poetry.org | python3 -

.PHONY: install
install:			## Install packages
	@echo "Installing packages..."
	poetry install

.PHONY: create_poetry_environment
create_poetry_environment:	## Create poetry environment
	@echo "Creating poetry environment..."
	poetry env use python3.12

# MISSING INSTALL node
# MISSING INSTALL npm
# MISSING INSTALL npx

#
# Day to day commands
#

.PHONY: generate_output_css
generate_output_css:  		## Generate Output CSS
	@echo "Generating output.css..."
	npx tailwindcss -i ./static/src/input.css -o ./static/src/output.css --watch

.PHONY: test
test:				## Run tests
	@echo "Running tests..."
	poetry run pytest

.PHONY: make_migrations
make_migrations:		## Make migrations
	@echo "Making migrations..."
	poetry run python manage.py makemigrations

.PHONY: migrate
migrate:			## Run migrations
	@echo "Running migrations..."
	poetry run python manage.py migrate

.PHONY: django_runserver
django_runserver: 		## Run Django server
	@echo "Running Django server..."
	poetry run python manage.py runserver

# LiveReload is a tool to automatically refresh your browser when files change.
# See: pyproject.toml
.PHONY: livereload
livereload: 			## Run livereload
	@echo "Running livereload..."
	poetry run python manage.py livereload

#
# Docker related commands
#
.PHONY: docker_compose_up
docker_compose_up:		## Run docker compose up running needed containers in the foreground
	docker compose up

.PHONY: docker_compose_pull
docker_compose_pull:		## Pull docker latest versions of images
	docker compose pull
