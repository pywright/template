from tests.helpers import Generate


def test_whenArtifactIsSet_expectBinaryInstalledToUsrBin(generate: Generate) -> None:
    project = generate(packaging="debian-jammy-arm64", artifact="distinctive-artifact")

    lines = (project / "debian/install").read_text().splitlines()

    assert lines == ["pkg/distinctive-artifact usr/bin"]
