import tomllib
from pathlib import Path
from typing import Any

import pytest

from tests.helpers import AUTHOR, EMAIL, Generate, choices


def load(project: Path) -> dict[str, Any]:
    return tomllib.loads((project / "pyproject.toml").read_text())


def test_whenArtifactIsSet_expectProjectName(generate: Generate) -> None:
    data = load(generate(artifact="my-cool-app"))

    assert data["project"]["name"] == "my-cool-app"


def test_whenArtifactHasHyphens_expectScriptPointsToUnderscoreModule(
    generate: Generate,
) -> None:
    data = load(generate(artifact="my-cool-app"))

    assert data["project"]["scripts"] == {"my-cool-app": "my_cool_app.cli:cli"}


def test_whenTitleIsSet_expectProjectDescription(generate: Generate) -> None:
    data = load(generate(__title="Distinctive Project Title"))

    assert data["project"]["description"] == "Distinctive Project Title"


def test_whenVersionIsSet_expectProjectVersion(generate: Generate) -> None:
    data = load(generate(__version="7.7.7"))

    assert data["project"]["version"] == "7.7.7"


def test_whenPythonIsSet_expectRequiresPython(generate: Generate) -> None:
    data = load(generate(__python="3.99"))

    assert data["project"]["requires-python"] == ">=3.99"


def test_whenAuthorIsSet_expectAuthorsEntry(generate: Generate) -> None:
    data = load(generate(__author=AUTHOR, __email=EMAIL))

    assert data["project"]["authors"] == [{"name": AUTHOR, "email": EMAIL}]


@pytest.mark.parametrize("license", choices()["license"])
def test_whenLicenseIsSet_expectLicenseFileReferenceResolves(
    generate: Generate, license: str
) -> None:
    project = generate(license=license)

    reference = load(project)["project"]["license"]

    assert reference == {"file": "LICENSE"}
    assert (project / reference["file"]).is_file()
