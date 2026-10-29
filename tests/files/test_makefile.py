from pathlib import Path

from tests.helpers import Generate

ARTIFACT = "my-cli"


def read_makefile(project: Path) -> str:
    return (project / "Makefile").read_text()


def test_whenArtifactIsSet_expectArtifactVariableRendered(generate: Generate) -> None:
    project = generate(artifact=ARTIFACT)

    assert f"ARTIFACT := {ARTIFACT}" in read_makefile(project).splitlines()


def test_whenArtifactIsSet_expectRunTargetUsesArtifactVariable(
    generate: Generate,
) -> None:
    project = generate(artifact=ARTIFACT)

    assert "\tuv run $(ARTIFACT) ${ARGS}" in read_makefile(project)
