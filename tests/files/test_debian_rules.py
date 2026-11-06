import os
from pathlib import Path

from tests.helpers import Generate


def rules_path(project: Path) -> Path:
    return project / "debian/rules"


def test_whenProjectIsGenerated_expectRulesExecutable(generate: Generate) -> None:
    assert os.access(rules_path(generate(packaging="debian-jammy-arm64")), os.X_OK)


def test_whenProjectIsGenerated_expectAutoStepsSkipped(generate: Generate) -> None:
    lines = (
        rules_path(generate(packaging="debian-jammy-arm64")).read_text().splitlines()
    )

    assert "override_dh_auto_clean:" in lines
    assert "override_dh_auto_build:" in lines
    assert "override_dh_auto_test:" in lines
    assert "override_dh_auto_install:" in lines
