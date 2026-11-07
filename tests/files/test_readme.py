from pathlib import Path

import pytest

from tests.helpers import Generate


def read_readme(project: Path) -> str:
    return (project / "README.md").read_text()


def test_whenTitleAndDescriptionAreSet_expectReadmeHeadingAndDescription(
    generate: Generate,
) -> None:
    project = generate(
        __title="Distinctive Project Title",
        __description="Distinctive project description for this test.",
    )

    content = read_readme(project)

    assert "# Distinctive Project Title" in content
    assert "Distinctive project description for this test." in content


def test_whenPackagingIsDebian_expectBuildOutputAndInstallDescribed(
    generate: Generate,
) -> None:
    content = read_readme(generate(packaging="debian-jammy-arm64"))

    assert "`make build` builds the `.deb` in a Docker image" in content
    assert "sudo apt install ./dist/*.deb\n" in content


def test_whenPackagingIsDebian_expectDockerRequirementsListed(
    generate: Generate,
) -> None:
    content = read_readme(generate(packaging="debian-jammy-arm64"))

    assert "https://docs.docker.com/engine/install/)" in content
    assert "https://docs.docker.com/engine/install/linux-postinstall/)" in content


def test_whenPackagingIsPython_expectBuildOutputAndInstallDescribed(
    generate: Generate,
) -> None:
    content = read_readme(generate(packaging="python"))

    assert "source distribution and wheel" in content
    assert "uv tool install dist/*.whl\n" in content


def test_whenPackagingIsPython_expectNoDebianSection(generate: Generate) -> None:
    content = read_readme(generate(packaging="python"))

    assert ".deb" not in content
    assert "Docker" not in content


@pytest.mark.parametrize("packaging", ["python", "debian-jammy-arm64"])
def test_whenPackagingIsSet_expectReleaseStepsDescribed(
    generate: Generate, packaging: str
) -> None:
    content = read_readme(generate(packaging=packaging))

    assert "## Releasing\n\nPush a `v*` tag" in content
