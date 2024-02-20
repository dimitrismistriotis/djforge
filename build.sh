#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
make install

# Convert static asset files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
make migrate
