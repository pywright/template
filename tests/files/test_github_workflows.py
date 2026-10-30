from tests.helpers import Generate


def test_whenProjectIsGenerated_expectCiWorkflowRunsMakeBuild(
    generate: Generate,
) -> None:
    project = generate()

    content = (project / ".github" / "workflows" / "ci.yml").read_text()

    assert "run: make build" in content


def test_whenProjectIsGenerated_expectCiWorkflowTokenIsReadOnly(
    generate: Generate,
) -> None:
    project = generate()

    content = (project / ".github" / "workflows" / "ci.yml").read_text()

    assert "permissions:\n  contents: read\n" in content


def test_whenProjectIsGenerated_expectSbomWorkflowKeepsGithubTokenExpression(
    generate: Generate,
) -> None:
    project = generate()

    content = (project / ".github" / "workflows" / "sbom.yml").read_text()

    assert "GH_TOKEN: ${{ github.token }}" in content
