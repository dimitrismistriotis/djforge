#
#
# References:
#
# https://stackoverflow.com/questions/5618615/check-if-a-program-exists-from-a-makefile
#
SHELL := /bin/bash

.SILENT: help

.PHONY: default
default: help

#
# Variables
#
UV_COMMAND_PREFIX := uv run python
GENERATE_SECRET_KEY := ${UV_COMMAND_PREFIX} manage.py generate_secret_key
# Note that there is not a trailing slash in the following variable for readability:
THEME_CSS_BASE_DIRECTORY := ./dj_theme/static/dj_theme/css


# The following fgrep will dynamically print all targets
# that have a comment beginning with two hashes including help.
.PHONY: help
help:				## Show help message.
	echo "Usage: make [target]"
	echo ""
	echo "Targets:"
	echo ""
	fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'


.PHONY: precommit_install
precommit_install:		## Install pre-commit hooks
	uv run pre-commit install

.PHONY: install
install:			## Install packages
	@echo "Installing packages..."
	uv sync

install_npm:			## Install npm packages
	@echo "Installing npm packages..."
	npm install


.PHONY: create_dot_env_file
create_dot_env_file:		## Create .env file
	@echo "Creating .env file..."
	echo "DEBUG=True" > .env
	${GENERATE_SECRET_KEY}  | tail -n 1 | uv run python -c "print(f'SECRET_KEY=\"{input()}\"')" >> .env


.PHONY: secret_key
secret_key:
	${GENERATE_SECRET_KEY}


.PHONY: update_dependencies
update_dependencies:		## Update Project dependencies
	@echo "Update Dependencies..."
	uv sync -U


.PHONY: update_react_email
update_react_email:		## Update React Email packages
	@echo "React Email..."
	cd dj_emails/react_email && npm update


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

#
# Development commands
#
.PHONY: collect_static
collect_static:			## Collect Static Files
	@echo "Collect Static..."
	${UV_COMMAND_PREFIX} manage.py collectstatic --no-input


build: install collect_static migrate	## Build the project


# Email templating
.PHONY: react_email
react_email:			## Run React Email to edit email templates
	@echo "React Email..."
	cd dj_emails/react_email && npm run dev


.PHONY: generate_email_templates
generate_email_templates:	## Generate React Email HTML and text templates
	@echo "React Email Export..."

	# HTML:
	cd dj_emails/react_email && \
		npm run export -- --outDir "../email_templates/html" --pretty true
	# Text:
	cd dj_emails/react_email && \
		npm run export -- --outDir "../email_templates/txt" --plainText true


#
# Day to day commands
#

.PHONY: generate_output_css
generate_output_css:  		## Generate Output CSS in watching for changes mode
	@echo "Generating output.css..."
	npx @tailwindcss/cli -i ./input.css -o ${THEME_CSS_BASE_DIRECTORY}/output.css --watch

.PHONY: test
test:				## Run tests
	@echo "Running tests..."
	uv run pytest


.PHONY: test_watch
test_watch:			## Run tests in watch mode (rerun tests when files change)
	@echo "Pytest Watch..."
	uv run ptw


.PHONY: test_recreate
test_recreate:			## Run tests creating the database, needed after migrations
	@echo "Running tests..."
	uv run pytest --create-db

.PHONY: migrations
migrations:		## Make migrations
	@echo "Making migrations..."
	${UV_COMMAND_PREFIX} manage.py makemigrations

.PHONY: migrate
migrate:			## Run migrations
	@echo "Running migrations..."
	${UV_COMMAND_PREFIX} manage.py migrate


.PHONY: django_runserver
django_runserver: 		## Run Django server
	@echo "Running Django server..."
	${UV_COMMAND_PREFIX} manage.py runserver


.PHONY: celery
celery:				## Run celery
	@echo "Running celery..."
	uv run celery -A djforge worker -l info


# LiveReload is a tool to automatically refresh your browser when files change.
# See: pyproject.toml
.PHONY: livereload
livereload: 			## Run livereload
	@echo "Running livereload..."
	${UV_COMMAND_PREFIX} manage.py livereload


.PHONY: shell
shell:              ## Run Django's shell_plus
	@echo "Running django shell..."
	${UV_COMMAND_PREFIX} manage.py shell_plus


.PHONY: dbshell
dbshell:            ## Run Django's dbshell
	@echo "Running Django's dbshell..."
	${UV_COMMAND_PREFIX} manage.py dbshell


#
# Run many web development make targets concurrently in one shell
# https://kylewbanks.com/blog/running-multiple-make-targets-concurrently
#
.PHONY: development_tmux_services
development_tmux_services:	## Run Docker Compose, Django server, celery, and a shell in tmux if there
	@echo ""
	@echo "Tmux Development Multiplexing..."
	@echo ""
	./development_assist/dev_env_tmux


#
# Run many web development make targets concurrently in one shell
# https://kylewbanks.com/blog/running-multiple-make-targets-concurrently
#
# Follow Up(s):
# - Perhaps add Celery here
#
.PHONY: runserver_plus_additional_services
runserver_plus_additional_services:	## Run Django server, generate_output_css and livereload together
	make -j django_runserver generate_output_css livereload


#
# Docker related commands
#
.PHONY: docker_compose_up
.PHONY: up
docker_compose_up up:		## Run docker compose up running needed containers in the foreground
	./development_assist/docker_compose_wrapper up


.PHONY: pull_docker_compose
pull_docker_compose:		## Pull docker latest versions of images
	./development_assist/docker_compose_wrapper pull
