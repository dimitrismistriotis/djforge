SHELL := /bin/bash

.SILENT: help

.PHONY: default
default: help

#
# Variables
#
GENERATE_SECRET_KEY := poetry run python manage.py generate_secret_key

# The following fgrep will dynamically print all targets
# that have a comment beginning with two hashes including help.
.PHONY: help
help:				## Show help message.
	echo "Usage: make [target]"
	echo ""
	echo "Targets:"
	echo ""
	fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

.PHONY: install_poetry
install_poetry:
	@echo "Installing poetry (source: https://python-poetry.org/docs/)..."
	curl -sSL https://install.python-poetry.org | python3 -

.PHONY: precommit_install
precommit_install:		## Install pre-commit hooks
	poetry run pre-commit install

.PHONY: install
install:			## Install packages
	@echo "Installing packages..."
	poetry install

install_npm:			## Install npm packages
	@echo "Installing npm packages..."
	npm install

.PHONY: create_poetry_environment
create_poetry_environment:	## Create poetry environment
	@echo "Creating poetry environment..."
	poetry env use python3.12

.PHONY: create_dot_env_file
create_dot_env_file:		## Create .env file
	@echo "Creating .env file..."
	echo "DEBUG=True" > .env
	${GENERATE_SECRET_KEY}  | tail -n 1 | poetry run python -c "print(f'SECRET_KEY=\"{input()}\"')" >> .env

.PHONY: secret_key
secret_key:
	${GENERATE_SECRET_KEY}

.PHONY: remove_containers_and_volumes
remove_containers_and_volumes:	## Remove containers and volumes related to the project, useful when you want to restart from scratch
	@echo "Removing containers..."
	@echo "Because action is destrictive, you need to confirm by typing 'yes' in uppercase"
	@read -p "Are you sure? " -n 3 -r; \
	if [[ $$REPLY == "YES" ]]; then \
		echo "Removing containers..."; \
		docker ps -a --filter "label=net.djforge" --format '{{.Names}}' | xargs docker rm; \
		docker volume ls --format '{{.Name}}' --filter "label=net.djforge" | xargs docker volume rm; \
	fi

# MISSING INSTALL node
# MISSING INSTALL npm
# MISSING INSTALL npx

#
# Development commands
#
.PHONY: collect_static
collect_static:			## Collect Static Files
	@echo "Collect Static..."
	poetry run python manage.py collectstatic --no-input

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
.PHONY: up
docker_compose_up up:		## Run docker compose up running needed containers in the foreground
	docker compose up

.PHONY: pull_docker_compose
pull_docker_compose:		## Pull docker latest versions of images
	docker compose pull
