from tests.helpers import Generate


def test_whenGenerated_expectPreCommitConfigGenerated(generate: Generate) -> None:
    project = generate()

    assert (project / ".pre-commit-config.yaml").is_file()
