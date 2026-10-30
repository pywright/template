# AGENTS.md: {{ cookiecutter.__title }}

Best practices for working in this project. Follow them when writing or
changing code.

## Commands

- `make run ARGS="..."`: run the CLI.
- `make lint`: lint and type-check.
- `make test`: run the tests.

Run `make lint` and `make test` before finishing a change.

## Python version

Use the one in `.python-version`. Do not use syntax or libraries that need a
newer one.

## Source code

### General

- **Zen of Python**: follow it ([PEP 20](https://peps.python.org/pep-0020/),
  or run `import this`).
- **Paths**: use `pathlib` instead of `os.path`.
- **Output**: use `logging` instead of `print`. Use `click.echo` for the CLI's
  intended output.
- **Data**: no mutable default arguments. Prefer dataclasses for plain data.
- **Secrets**: never commit them or include them in logs or error messages.

### Typing

- **Signatures**: typing is mandatory. Annotate every function and method
  parameter and return type, except `self` and `cls`.
- **Bodies**: annotate only when the type is not obvious. Do not annotate local
  variables whose type is clear from the assigned value.
- **Types**: use built-in generics and `X | None` where supported by the
  project's Python version. Avoid `Any` unless necessary.

### Imports

- **Classes**: import by name (`from module import Class`).
- **Functions**: import the module and call `module.function()`, so it is clear
  where a function comes from.
- **Aliases**: do not use `import x as y` or `from x import y as z` unless
  strictly necessary, such as to resolve a name conflict.

### Naming

- **Units**: quantities carry their unit as a suffix: `sleep_s`, `timeout_ms`,
  `max_size_bytes`, never `sleep`, `timeout` or `size`. This applies to
  variables, parameters, fields, config keys, CLI options and environment
  variables under our control. Preserve names required by external APIs. Keep
  one unit internally and convert at the boundary.

### Documentation

- **Docstrings**: optional. Write one only when the behavior is not obvious
  from the name and signature, and do not clog the code with them. There is no
  strict rule: the main public functions of a module or abstract base class
  methods, for example, often deserve some extra explanation. Use the Sphinx
  (reST) style: `:param name:`, `:returns:`, `:raises:`.
- **Comments**: only for non-trivial logic. Explain why, not what. Do not
  comment code that reads clearly on its own.

### Errors and CLI

- **Exceptions**: raise and catch specific exceptions. Handle them explicitly
  or propagate them. Do not use bare `except`.
- **CLI**: write normal output to stdout and errors to stderr, exit non-zero on
  failure, and provide a clear error message.

## Tests

### Layout and naming

- **Layout**: tests live in `tests/{{ cookiecutter.__module }}/`, one module
  per source module (`test_cli.py` tests `cli.py`).
- **Names**: `test_when<Condition>_expect<Outcome>`, camelCase after the
  prefix.
  - `<Condition>` is the input state, written as `<Subject>Is<State>`
    (`whenTimeoutIsSet`, `whenInputIsEmpty`, `whenFileIsMissing`). Use `Set`
    and `Unset` for optional values.
  - `<Outcome>` names what is observed: `expectXReturned` for values,
    `expectXRaised` for errors, `expectXWritten` for side effects.
  - Do not put test data or parametrized values in names.

### Writing tests

- **Structure**: use `# Prepare`, `# Act` and `# Assert` comments where those
  phases apply. Include only the comments needed for the test; omit phases that
  require no code.
- **Parametrization**: use `pytest.mark.parametrize` instead of loops.
- **Bug fixes**: add a regression test that fails without the fix.

### Tools

- **Focused tools**: prefer well-established testing tools when they fit the
  behavior under test: `pyfakefs` for filesystem interactions, `freezegun` for
  time-dependent behavior and `requests-mock` for HTTP requests made with
  Requests. Prefer them over built-in `mock` or `patch` when a suitable tool
  exists.
- **Network**: avoid real network access.

## Workflow

- **Changes**: follow existing patterns, and keep changes small and focused.
- **Approval**: ask before adding a dependency.
- **Generated files**: do not edit them or the lockfile by hand.
- **Commits**: use Conventional Commits for commit messages.
- **This file**: update it in the same change when you change commands,
  tooling or conventions.
