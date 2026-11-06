from tests.helpers import Generate


def test_whenPackagingIsDebian_expectDebianRulesRendered(generate: Generate) -> None:
    project = generate(packaging="debian-jammy-arm64")

    assert "pkg/" in (project / ".gitignore").read_text().splitlines()


def test_whenPackagingIsPython_expectDebianRulesNotRendered(generate: Generate) -> None:
    project = generate(packaging="python")

    assert "pkg/" not in (project / ".gitignore").read_text().splitlines()
