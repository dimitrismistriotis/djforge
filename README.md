# Readme

## References

[Tailwind CSS Django - Flowbite](https://flowbite.com/docs/getting-started/django/)

[The Ruff Formatter](https://docs.astral.sh/ruff/)

[FavIcons](https://www.favicon-generator.org/)

Can use this one to generate specifics for your project

### Editors

We use the community edition of [PyCharm](https://www.jetbrains.com/pycharm/) and [VS Code](https://code.visualstudio.com/).

Settings are included and stored in the `.idea` and `.vscode` folders respectively. You might want to change them
or completely remove them from the project based on which IDE/editor you use and how.
After some deliberation, we decided to include them in order to make development faster
for those who use or will use either of these editors.

### Commit messages

We use [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/). Commitizen is used to help with this, added already in the dev dependencies of the project. To use commitizen run `poetry run cz commit` instead of `git commit` or add an alias to your shell config file (e.g. `.bashrc` or `.zshrc`), such as `alias cz="poetry run cz"`.

## Dependencies

Using Python 3.12 and higher.

Poetry is used for dependency management. Install it with `pip install poetry`.
