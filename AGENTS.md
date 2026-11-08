# AGENTS.md: Template tests

How to write tests for this Cookiecutter template. There are four kinds, and
all are required:

1. **File existence**: one test lists every generated file.
2. **Variable tests**: one module checks how `cookiecutter.json` derives its
   variables.
3. **Per-file tests**: content and rendered variables of a file, only for files
   with something to check beyond existing.
4. **Build tests**: every option of every choice generates a project that
   passes `make build`.

A full-project test can pass while a single file is wrong (wrong content, stale
value, wrong variable). Per-file tests pinpoint *which* file and *which*
variable broke; build tests guarantee the *whole project* works. Neither
replaces the other.

## Layout

```
tests/
  conftest.py            # generate and render fixtures
  helpers.py             # choices(), debian_packagings(), matrix(), variants(), case_id()
  files/
    test_rendered.py     # expected files exist, no unrendered syntax
    test_<file>.py       # per-file content tests (only where needed)
  variables/
    test_variables.py    # derived cookiecutter.json variables
  builds/                # build tests over the parameter variants
    test_build.py
  hooks/                 # hook tests (separate)
  extensions/            # extension tests (separate)
```

## Tools

- `pytest` + `pytest-cookies` (the `cookies` fixture) for generating
  projects.
- Run `make test` (all tests), `make test-fast` (everything except the slow
  `build` tests), `make test-amd64` (build tests for amd64 and the Python
  package) or `make test-arm64` (build tests for arm64). CI runs each build
  target on a runner of its architecture.
- Test names: `test_when<Condition>_expect<Outcome>`, camelCase after the
  prefix.
  - `<Condition>` is the input state, written as `<Subject>Is<State>`
    (`whenLicenseIsSet`, `whenTitleIsSet`, `whenArtifactIsInvalid`). Use `Set`
    and `Unset` for variables. Do not put test data ("Distinctive") in names.
  - `<Outcome>` names what is observed: `expectXRendered` for content,
    `expectXExists` for presence, `expectGenerationAborted` for failures.
  - Use `whenProjectIsGenerated` only when nothing varies.
  - Parametrized values never appear in the name.
- Annotate every test: fixtures with `Generate` / `Render`, return `-> None`.
- Ruff ignores `D`, `PL`, `S` in tests; no docstrings required.

## Fixtures and helpers

Already implemented; reuse them, do not reimplement them.

- **`generate` fixture** (`tests/conftest.py`): generates a project with
  `extra_context`, asserts generation succeeded and returns the project path.
- **`render` fixture** (`tests/conftest.py`): renders the `cookiecutter.json`
  variables (public and `__private`) without generating files; returns the
  rendered dict.
- **`gitconfig` fixture** (`tests/conftest.py`, autouse): isolates tests from
  the machine's git config. Do not remove it.
- **`build` marker**: registered in `tests/conftest.py`.
- **`choices()` / `debian_packagings()` / `matrix()` / `variants()` /
  `case_id()`** (`tests/helpers.py`): the choice variables, the `packaging`
  choices that build a Debian package, every combination of the choices, the
  fewest cases that use every option once (all derived from
  `cookiecutter.json`) and a readable pytest id for a case.

## 1. File existence

`EXPECTED_FILES` in `tests/files/test_rendered.py` is the single list of paths
every generated project must contain (`{module}` stands for the package name).
Paths generated only for one option value get their own list next to it (e.g.
`DEBIAN_FILES` for `debian` packaging), and the hook that removes them otherwise is
tested in `tests/hooks/`.

- Per-file modules do not assert that their file exists; reading it fails if it
  does not.
- Files that only need to exist get a line in `EXPECTED_FILES` and no module of
  their own.
- Unrendered template syntax (`{{`, `{%`, `cookiecutter.`) is checked there for
  every file and combination. Do not repeat that check in per-file tests.

## 2. Variables

`tests/variables/test_variables.py` is the only place that tests the rules that
compute variables in `cookiecutter.json`. Cover every branch of the rule,
including edge cases.

Per-file tests only check *wiring*: that the file shows the value of the
variable. Pass the private variable explicitly
(`generate(__title="Distinctive Title")`) and never repeat the normalization
cases there. When a variable's rule changes in `cookiecutter.json`, change its
cases here and nowhere else.

## 3. Per-file tests

Create `tests/files/test_<file>.py` only when the file has content or variables
to check. Each module checks:

1. The **variables are rendered correctly** where they appear.
2. The **content that depends on an option value** is right for each value, and
   nothing is **leaked** from another option (e.g. only one `LICENSE`).

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

1. Add its path to `EXPECTED_FILES` in `tests/files/test_rendered.py`.
2. List which `cookiecutter.json` variables affect the file. If none and its
   content is not worth pinning, stop here.
3. Otherwise create `tests/files/test_<file>.py`, parametrize over the option
   values that change the file, and assert each variable's rendered value in
   the exact place it appears.
4. If the file needs a new derived variable, add its rule to
   `tests/variables/test_variables.py`.

## 4. Build tests

For **every** option of every choice, the generated project passes `make
build`, the command CI runs.

- **The cases are derived from `cookiecutter.json`** (`choices()`,
  `variants()`), never hardcoded. Adding a new option or choice must
  automatically add build cases.
- **Use every option once, not every combination**: builds are slow and every
  combination grows with the product of the options, while `variants()` grows
  with the largest one. Content that depends on a combination of options is
  checked in per-file tests over `matrix()` instead.
- If a combination is invalid, forbid it in the `pre_gen_project` hook so it
  fails at generation instead.
- **Run the real command**: `make build` in the generated project, no mocks
  and no patched Makefile.
- **Show the output on failure**: include stdout and stderr in the assertion
  message.
- **Skips must be explicit and justified** (e.g. a choice that needs an
  external tool missing locally). CI must run every case with no skips.
- **Docker is required**: the `debian` cases fail without it, they do not skip.

## Workflows

After adding or removing an action in a workflow, update the lockfile next to
it:

- **Root**: run `gh actions-lock`.
- **Template**: generate a project for each packaging, run `gh actions-lock`
  there and copy the result to
  `{{cookiecutter.artifact}}/.github/workflows/actions.lock`, keeping the Jinja
  blocks for actions used by one packaging only.
  `tests/files/test_actions_lock.py` checks the result.

## Out of scope

- Hooks and extensions: tested separately, not through the
  `generate` fixture.
