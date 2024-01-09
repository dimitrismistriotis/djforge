# Contributing

## Commit messages

We use [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).
Commitizen is used to help with this, added already in the dev dependencies of
the project. To use commitizen run `poetry run cz commit` instead of `git commit`
or add an alias to your shell config file (e.g. `.bashrc` or `.zshrc`), such as
`alias cz="poetry run cz"`.

## Testing

We use
[pytest](
https://pragprog.com/titles/bopytest2/python-testing-with-pytest-second-edition/)
for testing. To run the tests, run `make test`. Bearing in mind that testing is
a tool and not a doctrine, add tests whenever this is necessary or a considerable size
chunk of code is added.
