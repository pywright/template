from pathlib import Path

import pytest

from tests.helpers import Generate, case_id, matrix

ARTIFACT = "distinctive-artifact"
MODULE = "distinctive_artifact"

EXPECTED_FILES = (
    ".editorconfig",
    ".github/workflows/ci.yml",
    ".github/workflows/sbom.yml",
    ".gitignore",
    ".pre-commit-config.yaml",
    ".python-version",
    "LICENSE",
    "Makefile",
    "README.md",
    "pyproject.toml",
    "src/{module}/__init__.py",
    "src/{module}/cli.py",
    "src/{module}/py.typed",
    "tests/{module}/conftest.py",
    "tests/{module}/test_cli.py",
)

LEFTOVERS = ("{{", "{%", "cookiecutter.")
ALLOWED_EXCEPTIONS = {
    ".github/workflows/sbom.yml": ("${{ github.token }}",),
}


def generated_files(project: Path) -> list[Path]:
    return [
        path
        for path in project.rglob("*")
        if path.is_file() and ".git" not in path.relative_to(project).parts
    ]


@pytest.mark.parametrize("context", matrix(), ids=case_id)
def test_whenProjectIsGenerated_expectNoUnrenderedSyntaxInAnyFile(
    generate: Generate, context: dict[str, str]
) -> None:
    project = generate(**context)

    offenders = []
    for path in generated_files(project):
        relative = str(path.relative_to(project))
        try:
            text = path.read_text()
        except UnicodeDecodeError:
            text = ""  # binary file: only its name is checked
        for expression in ALLOWED_EXCEPTIONS.get(relative, ()):
            text = text.replace(expression, "")
        if any(token in relative or token in text for token in LEFTOVERS):
            offenders.append(relative)

    assert not offenders, f"unrendered template syntax in: {offenders}"


@pytest.mark.parametrize("context", matrix(), ids=case_id)
def test_whenProjectIsGenerated_expectEveryExpectedFileExists(
    generate: Generate, context: dict[str, str]
) -> None:
    project = generate(**context, artifact=ARTIFACT)

    missing = [
        path
        for path in (template.format(module=MODULE) for template in EXPECTED_FILES)
        if not (project / path).is_file()
    ]

    assert not missing, f"missing generated files: {missing}"
