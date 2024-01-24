# Readme

## References

[Postgres](https://www.postgresql.org/)

[Tailwind CSS Django - Flowbite](https://flowbite.com/docs/getting-started/django/)

[Flowbite](https://flowbite.com/docs/getting-started/introduction/)

[The Ruff Formatter](https://docs.astral.sh/ruff/)

[FavIcons](https://www.favicon-generator.org/)

[Landwind](https://github.com/themesberg/landwind) for the landing page

Can use this one to generate specifics for your project

[LiveReload Server](https://github.com/tjwalch/django-livereload-server)

### Editors

We use the community edition of [PyCharm](https://www.jetbrains.com/pycharm/) and [VS Code](https://code.visualstudio.com/).

Settings are included and stored in the `.idea` and `.vscode` folders respectively. You might want to change them
or completely remove them from the project based on which IDE/editor you use and how.
After some deliberation, we decided to include them in order to make development faster
for those who use or will use either of these editors.

## Dependencies

Using Python 3.12 and higher.

Poetry is used for dependency management. Install it with `pip install poetry`.

## Postgres

We decided to use Postgres as the database for this project as it is the most popular
RDBMS for Django projects, also one of the most popular RDBMS in general.

For most applications a RDBMS is a good-enough choice, which makes it a good default
to kickstart your project.

## Day to Day

## Run Database and related services with Docker Compose

**Purpose**: To have a database and related services running in the background

**How**: 

```shell
make up
```

### Live Reload

**Purpose**: To have the browser reload automatically when a change is made to the
code, makes it easier to develop CSS + HTML changes

**How**:

```shell
make livereload
```
