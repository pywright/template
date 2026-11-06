from pathlib import Path

from tests.helpers import Generate

ARTIFACT = "distinctive-artifact"
VERSION = "7.7.7"


def read_changelog(project: Path) -> list[str]:
    return (project / "debian/changelog").read_text().splitlines()


def test_whenArtifactAndVersionAreSet_expectEntryHeadingRendered(
    generate: Generate,
) -> None:
    lines = read_changelog(
        generate(packaging="debian-jammy-arm64", artifact=ARTIFACT, __version=VERSION)
    )

    assert lines[0] == f"{ARTIFACT} ({VERSION}) UNRELEASED; urgency=medium"


def test_whenAuthorIsSet_expectTrailerRendered(generate: Generate) -> None:
    lines = read_changelog(
        generate(
            packaging="debian-jammy-arm64",
            __author="Jane Doe",
            __email="jane.doe@example.com",
        )
    )

    assert lines[-1].startswith(" -- Jane Doe <jane.doe@example.com>  ")
