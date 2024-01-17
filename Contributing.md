# Contributing

This is specific for the base project, **DJ Forge**. You can use any part
of it on your derived project, or change it accordingly.

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

## Development Patterns

### Handler Pattern

We decided to use the handler pattern as an intermediate between
UI endpoints and resources handling business logic.

A short edited article generated initially from ChatGPT follows
to have as a quick reference.

The handler pattern in Python is a design approach where a handler class acts as an
intermediary between different parts of the application. This pattern is particularly
useful for separating concerns, managing complexity, and improving code
maintainability. Let's break down how it works:

#### Detailing Handler Pattern

**Core Components of the Handler Pattern**

- **Models**: Represent the data structure, usually mapping to database tables. 
They encapsulate the data and its direct manipulation.
- **APIs**: Provide an interface for external or internal clients to interact with the 
application's data and services.
- **UI Code**: The front-end part of the application, which interacts with the user.
- **Handler Class**: Sits in between these components, acting as a mediator or a
controller. It handles the business logic, processes requests from the UI, interacts
with the models, and prepares responses.
- **Responsibilities of the Handler Class**
- **Request Processing**: It accepts requests from the UI or API layer, processes them,
and determines the appropriate action or response.
- **Business Logic**: Encapsulates the core business logic of the application,
keeping it separate from the UI and model concerns. This might include validation,
calculations, decision making, etc.
- **Model Interaction**: Communicates with models to retrieve, update, or manipulate
data. This includes database queries, data manipulation, and transactions.
- **Response Preparation**: Once the business logic is processed and the model
interactions are complete, the handler prepares and sends the response back
to the UI or API layer.
- **Integration and External Calls**: Handles integration with external services or APIs.
This can include fetching data from other services, sending notifications, etc.

**Advantages of Using Handler Pattern**

Separation of Concerns: By decoupling business logic from the UI and model layers,
the code becomes more organized and easier to manage.

- **Reusability**: Handlers can be designed to be reusable across different parts of
the application.
- **Maintainability**: Changes in the business logic or in the data layer can be managed
within the handlers without affecting other parts of the application.
- **Testability**: Independent handlers are easier to unit test as they can be isolated
from the rest of the application.

**Conclusion**

The handler pattern is a powerful way to structure a Python application for better
separation of concerns, maintainability, and clarity. By centralizing business logic
and interactions in handler classes, developers can create more organized
and testable codebases.
