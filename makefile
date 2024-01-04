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