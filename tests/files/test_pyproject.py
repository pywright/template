import tomllib
from pathlib import Path
from typing import Any

import pytest

from tests.helpers import Generate, choices


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


@pytest.mark.parametrize(
    ("title", "description"),
    [
        ("Well-Known", "Well-Known"),
        ("  Extra   inner   spaces  ", "Extra inner spaces"),
        ("Ends with dot.", "Ends with dot"),
        ("Dot after space .", "Dot after space"),
    ],
)
def test_whenTitleIsSet_expectNormalizedDescription(
    generate: Generate, title: str, description: str
) -> None:
    data = load(generate(title=title))

    assert data["project"]["description"] == description


def test_whenVersionIsSet_expectProjectVersion(generate: Generate) -> None:
    data = load(generate(__version="7.7.7"))

    assert data["project"]["version"] == "7.7.7"


def test_whenAuthorIsSet_expectAuthorsEntry(generate: Generate) -> None:
    data = load(generate(__author="Jane Doe", __email="jane.doe@example.com"))

    assert data["project"]["authors"] == [
        {"name": "Jane Doe", "email": "jane.doe@example.com"}
    ]


@pytest.mark.parametrize("license_", choices()["license"])
def test_whenAnyLicenseIsChosen_expectLicenseFileReferenceResolves(
    generate: Generate, license_: str
) -> None:
    project = generate(license=license_)

    reference = load(project)["project"]["license"]

    assert reference == {"file": "LICENSE"}
    assert (project / reference["file"]).is_file()
