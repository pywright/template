# AGENTS.md: Template tests

How to write tests for this Cookiecutter template. There are two kinds, and
both are required:

1. **Per-file tests**: each generated file is checked on its own.
2. **Build tests**: every valid parameter combination generates a project
   that passes `make build`.

## Principle

A full-project test can pass while a single file is wrong (wrong content, stale
value, wrong variable). So tests are split by purpose:

- Per-file tests pinpoint *which* file and *which* variable broke.
- Build tests guarantee the *whole project* works, whatever parameters are
  passed.

Neither replaces the other.

## Layout

```
tests/
  conftest.py            # shared generate fixture
  helpers.py             # choices() and matrix() read from cookiecutter.json
  files/                 # per-file tests
    test_<file>.py       # one module per generated file
  builds/                # build tests over the parameter matrix
    test_build.py
  hooks/                 # hook tests (separate)
  extensions/            # extension tests (separate)
```

## Tools

- `pytest` + `pytest-cookies` (the `cookies` fixture) for generating
  projects.
- Run `make test` (all tests) or `make test-fast` (everything except the
  slow `build` tests).
- Test names: `test_whenXxx_expectYyy`.
- Type every signature: fixture arguments (e.g. `generate: Generate`,
  `cookies: Cookies`) and return types (`-> None` for tests).
- Ruff ignores `D`, `PL`, `S` in tests; no docstrings required.

## Already implemented

Reuse these; do not reimplement them.

- **`generate` fixture** (`tests/conftest.py`): generates a project with
  `extra_context`, asserts generation succeeded and returns the project path.
  Type it as `Generate` (`tests/helpers.py`).
- **`gitconfig` fixture** (`tests/conftest.py`, autouse): isolates tests from
  the machine's git config. Do not remove it.
- **`build` marker**: registered in `tests/conftest.py`.
- **`choices()` / `matrix()`** (`tests/helpers.py`): the choice variables and
  every combination of them, derived from `cookiecutter.json`.
- **Unrendered-syntax check**: `tests/files/test_rendered.py`, runs over every
  generated file for every combination from `matrix()`.
- **Per-file tests**: `tests/files/`, one module per generated file.
- **Build test**: `tests/builds/test_build.py`, parametrized over `matrix()`.

## 1. Per-file tests

One module per generated file: `tests/files/test_<file>.py`.

Each module checks:

1. The **correct file** is generated for each option value that affects it
   (or is absent when it should be).
2. The **variables are rendered correctly** where they appear.
3. Nothing is **leaked** from another option.

Unrendered template syntax (`{{`, `{%`, `cookiecutter.`) is checked once, for
every generated file and every parameter combination, by
`tests/files/test_rendered.py`. Do not repeat that check in per-file tests.

Rules:

- **Generate once per case**, read only the file under test.
- **Pass every variable you assert on explicitly**, using the exact names in
  `cookiecutter.json`. This works for private variables too (e.g.
  `generate(__author="Jane Doe")`), so never rely on defaults or the machine's
  git config.
- **Use distinctive values** so a match can't be a coincidence with a default.
- **Assert specific lines or fragments**, not whole-file snapshots. Snapshots
  hide which variable broke and fail on harmless edits.
- **Parametrize over every option value** that affects the file. When a new
  choice is added to `cookiecutter.json`, extend the parametrization in the
  same change.
- Keep tests fast and independent: no shared state between generated
  projects.

### Adding tests for a new file

1. Create `tests/files/test_<file>.py`.
2. List which `cookiecutter.json` variables affect the file.
3. Parametrize over the option values that change the file or its content.
4. Assert each variable's rendered value in the exact place it appears.

No test is needed for unrendered syntax; the central test already covers the
new file.

## 2. Build tests

For **any** valid combination of parameters, the generated project passes
`make build`. Already implemented in `tests/builds/test_build.py`.

Rules:

- **The matrix is derived from `cookiecutter.json`** (`matrix()`), never
  hardcoded. Adding a new option or choice must automatically add build cases.
  Do not filter combinations out; if one is invalid, forbid it in the
  `pre_gen_project` hook so it fails at generation instead.
- **Run the real command**: `make build` in the generated project, no mocks and no
  patched Makefile.
- **Show the output on failure**: include stdout and stderr in the assertion
  message.
- **Skips must be explicit and justified** (e.g. a choice that needs an
  external tool missing locally). CI must run every case with no skips.

## Out of scope

- Hooks and extensions: tested separately, not through the
  `generate` fixture.
