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
