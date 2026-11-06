from pathlib import Path

from tests.helpers import Generate

ARTIFACT = "distinctive-artifact"
TITLE = "Distinctive Title"
DESCRIPTION = "Distinctive description."


def read_control(project: Path) -> list[str]:
    return (project / "debian/control").read_text().splitlines()


def test_whenArtifactIsSet_expectSourceAndPackageRendered(generate: Generate) -> None:
    lines = read_control(generate(packaging="debian-jammy-arm64", artifact=ARTIFACT))

    assert f"Source: {ARTIFACT}" in lines
    assert f"Package: {ARTIFACT}" in lines


def test_whenAuthorIsSet_expectMaintainerRendered(generate: Generate) -> None:
    lines = read_control(
        generate(
            packaging="debian-jammy-arm64",
            __author="Jane Doe",
            __email="jane.doe@example.com",
        )
    )

    assert "Maintainer: Jane Doe <jane.doe@example.com>" in lines


def test_whenTitleIsSet_expectSynopsisRendered(generate: Generate) -> None:
    lines = read_control(generate(packaging="debian-jammy-arm64", __title=TITLE))

    assert f"Description: {TITLE}" in lines


def test_whenDescriptionIsSet_expectLongDescriptionRendered(
    generate: Generate,
) -> None:
    lines = read_control(
        generate(
            packaging="debian-jammy-arm64", __title=TITLE, __description=DESCRIPTION
        )
    )

    synopsis = lines.index(f"Description: {TITLE}")
    assert lines[synopsis + 1] == f" {DESCRIPTION}"


def test_whenDebhelperIsSet_expectBuildDependsRendered(generate: Generate) -> None:
    lines = read_control(generate(packaging="debian-jammy-arm64", __debhelper="99"))

    assert "Build-Depends: debhelper-compat (= 99)" in lines


def test_whenStandardsIsSet_expectStandardsVersionRendered(generate: Generate) -> None:
    lines = read_control(generate(packaging="debian-jammy-arm64", __standards="9.9.9"))

    assert "Standards-Version: 9.9.9" in lines
