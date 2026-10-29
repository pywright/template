from pathlib import Path

import pytest

from tests.helpers import Generate, matrix

LEFTOVERS = ("{{", "{%", "cookiecutter.")


def generated_files(project: Path) -> list[Path]:
    return [
        path
        for path in project.rglob("*")
        if path.is_file() and ".git" not in path.relative_to(project).parts
    ]


@pytest.mark.parametrize("context", matrix(), ids=lambda c: "-".join(c.values()))
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
        if any(token in relative or token in text for token in LEFTOVERS):
            offenders.append(relative)

    assert not offenders, f"unrendered template syntax in: {offenders}"
