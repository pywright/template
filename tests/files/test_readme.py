from pathlib import Path

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


def test_whenPackagingIsDeb_expectDebSectionWithTargetRendered(
    generate: Generate,
) -> None:
    project = generate(
        packaging="debian-jammy-arm64",
        __codename="distinctive-codename",
        __arch="distinctive-arch",
        __standards="distinctive-standards",
    )

    content = read_readme(project)

    assert "`.deb` for Ubuntu distinctive-codename, distinctive-arch" in content


def test_whenPackagingIsDeb_expectDockerRequirementsListed(generate: Generate) -> None:
    content = read_readme(generate(packaging="debian-jammy-arm64"))

    assert "https://docs.docker.com/engine/install/)" in content
    assert "https://docs.docker.com/engine/install/linux-postinstall/)" in content


def test_whenPackagingIsPython_expectBuildOutputDescribed(generate: Generate) -> None:
    content = read_readme(generate(packaging="python"))

    assert "source distribution and wheel" in content


def test_whenPackagingIsPython_expectNoDebSection(generate: Generate) -> None:
    content = read_readme(generate(packaging="python"))

    assert ".deb" not in content
    assert "Docker" not in content
