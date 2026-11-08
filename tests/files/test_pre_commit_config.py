from pathlib import Path

from tests.helpers import Generate

ROOT_CONFIG = Path(__file__).parents[2] / ".pre-commit-config.yaml"


def test_whenProjectIsGenerated_expectSameHooksAsTemplate(generate: Generate) -> None:
    content = (generate() / ".pre-commit-config.yaml").read_text()

    # The template config only adds an exclude line for the template directory.
    assert ROOT_CONFIG.read_text().endswith(content)
