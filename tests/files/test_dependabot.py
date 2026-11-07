from pathlib import Path

import pytest

from tests.helpers import Generate


def read_dependabot(project: Path) -> str:
    return (project / ".github/dependabot.yml").read_text()


@pytest.mark.parametrize("packaging", ["python", "debian-jammy-arm64"])
def test_whenPackagingIsSet_expectActionsUvAndPreCommitUpdated(
    generate: Generate, packaging: str
) -> None:
    content = read_dependabot(generate(packaging=packaging))

    assert "  - package-ecosystem: github-actions\n" in content
    assert "  - package-ecosystem: uv\n" in content
    assert "  - package-ecosystem: pre-commit\n" in content


def test_whenPackagingIsDebian_expectDockerUpdated(generate: Generate) -> None:
    content = read_dependabot(generate(packaging="debian-jammy-arm64"))

    assert "  - package-ecosystem: docker\n    directory: /packaging\n" in content


def test_whenPackagingIsPython_expectDockerNotUpdated(generate: Generate) -> None:
    content = read_dependabot(generate(packaging="python"))

    assert "docker" not in content
