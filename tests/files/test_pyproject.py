import tomllib
from pathlib import Path
from typing import Any

import pytest

from tests.helpers import Generate, choices


def load(project: Path) -> dict[str, Any]:
    return tomllib.loads((project / "pyproject.toml").read_text())


def test_whenProjectIsGenerated_expectUvBuildBackend(generate: Generate) -> None:
    data = load(generate())

    assert data["build-system"]["build-backend"] == "uv_build"


def test_whenPackagingIsDebian_expectPyinstallerInDebianGroup(
    generate: Generate,
) -> None:
    data = load(generate(packaging="debian-jammy-arm64"))

    assert any(
        dependency.startswith("pyinstaller>=")
        for dependency in data["dependency-groups"]["deb"]
    )


def test_whenPackagingIsPython_expectNoDebianGroup(generate: Generate) -> None:
    data = load(generate(packaging="python"))

    assert "deb" not in data["dependency-groups"]


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
    data = load(generate(__author="Jane Doe", __email="jane.doe@example.com"))

    assert data["project"]["authors"] == [
        {"name": "Jane Doe", "email": "jane.doe@example.com"}
    ]


@pytest.mark.parametrize("license", choices()["license"])
def test_whenLicenseIsSet_expectLicenseExpressionAndFileRendered(
    generate: Generate, license: str
) -> None:
    data = load(generate(license=license))

    assert data["project"]["license"] == license
    assert data["project"]["license-files"] == ["LICENSE"]
