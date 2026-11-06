from tests.helpers import Generate


def test_whenTitleAndModuleAreSet_expectAgentsGuidanceUsesRenderedValues(
    generate: Generate,
) -> None:
    project = generate(
        artifact="distinctive-agent-project",
        __title="Distinctive Agent Project",
    )

    content = (project / "AGENTS.md").read_text()

    assert "# AGENTS.md: Distinctive Agent Project" in content
    assert "tests/distinctive_agent_project/" in content


def test_whenPackagingIsDeb_expectDebCommandListed(generate: Generate) -> None:
    content = (generate(packaging="debian-jammy-arm64") / "AGENTS.md").read_text()

    assert "- `make build`: build the Debian package (needs Docker).\n" in content
    assert "- `make shell`: open a shell in the image that builds it.\n" in content
    assert "- `make pkg`: build the Debian package, inside `make shell`.\n" in content


def test_whenPackagingIsPython_expectBuildCommandListed(generate: Generate) -> None:
    content = (generate(packaging="python") / "AGENTS.md").read_text()

    assert "- `make build`: build the source distribution and wheel.\n" in content


def test_whenPackagingIsPython_expectNoDebCommands(generate: Generate) -> None:
    content = (generate(packaging="python") / "AGENTS.md").read_text()

    assert "Debian" not in content
    assert "make pkg" not in content
    assert "make shell" not in content
