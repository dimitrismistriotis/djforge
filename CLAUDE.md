# DJ Forge Commands & Code Style Guide

## Essential Commands

- Run tests: `make test`
- Run single test: `ENVIRONMENT='test' uv run pytest path/to/test_file.py::TestClass::test_method -v`
- Lint: `uv run ruff check .` or `uv run ruff check path/to/file.py`
- Format: `uv run ruff format .`
- Format HTML files: `uv run djhtml .` or `uv run djhtml path/to/file.html`
- Sort imports: `uv run isort .`
- Run dev server: `make runserver_plus_additional_services`
- Create migrations: `make migrations`
- Apply migrations: `make migrate`

## Code Style

- **Imports**: Use isort with Django profile. Order: FUTURE,STDLIB,THIRDPARTY,DJANGO,FIRSTPARTY,LOCALFOLDER
  Imports should be sorted alphabetically within each group.
  Imports should also be relative to the module they are in if they belong to the same module.
  Import one item per line
- **Formatting**: Follow PEP 8 with ruff formatter (enforced by pre-commit hooks)
- **Indentation**: Follow `.editorconfig` for everything
- **Docstrings**: Use pydocstyle conventions, required on all public modules, classes, and functions
- **Types**: Use type hints where appropriate
- **Naming**: Use descriptive names following Django conventions (snake_case for functions/variables, PascalCase for classes)
- **Error Handling**: Use specific exceptions and proper error messages. Be verbose on exception names, for example `except Exception as exception`, not `except Exception as e`
- **Testing**:
  - Use pytest fixtures from conftest.py else use it with model-bakery for test data.
  - Mark tests with appropriate markers. Hint tests to return "None".
  - Add hints to all test functions.
  - All imports should be at the top of the file.
  - Use the 'mocker' fixture of pytest whenever mocks are created.
  - Create classes for the test cases.
- When creating Models (`models.Model`) add a queryset on top of each model with the same name prefixed with `QuerySet`. Model should have a `objects = <model_name>QuerySet.as_manager()` entry.
  Also add `id = models.BigAutoField(primary_key=True)` to each one so that id can be discovered from editors.
