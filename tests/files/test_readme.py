from tests.helpers import Generate


def test_whenTitleAndDescriptionAreSet_expectReadmeHeadingAndDescription(
    generate: Generate,
) -> None:
    project = generate(
        __title="Distinctive Project Title",
        __description="Distinctive project description for this test.",
    )

    content = (project / "README.md").read_text()

    assert "# Distinctive Project Title" in content
    assert "Distinctive project description for this test." in content
