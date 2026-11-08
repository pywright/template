import re
from pathlib import Path

import pytest

from tests.helpers import Generate

# `owner/repo[/path]@ref` in a workflow; the lockfile records `owner/repo@ref`.
USES = re.compile(r"uses: ([\w-]+/[\w.-]+)(?:/\S+)?(@\S+)$", re.MULTILINE)
PINNED = re.compile(r"^    '(.+@.+)':$", re.MULTILINE)
SETUP_UV = "astral-sh/setup-uv@"


def read_lockfile(project: Path) -> str:
    return (project / ".github" / "workflows" / "actions.lock").read_text()


@pytest.mark.parametrize("packaging", ["python", "debian-jammy-arm64"])
def test_whenPackagingIsSet_expectEveryActionLockedOnce(
    generate: Generate, packaging: str
) -> None:
    project = generate(packaging=packaging)
    lockfile = read_lockfile(project)

    used = {
        path.name: sorted({repo + ref for repo, ref in USES.findall(path.read_text())})
        for path in sorted((project / ".github" / "workflows").glob("*.yml"))
    }
    workflows = "".join(
        f"    '.github/workflows/{name}':\n"
        + "".join(f"        - '{action}'\n" for action in actions)
        for name, actions in used.items()
    )

    assert f"\nworkflows:\n{workflows}dependencies:\n" in lockfile
    assert PINNED.findall(lockfile) == sorted(set().union(*used.values()))


def test_whenPackagingIsPython_expectSetupUvLocked(generate: Generate) -> None:
    lockfile = read_lockfile(generate(packaging="python"))

    assert f"        - '{SETUP_UV}" in lockfile
    assert f"\n    '{SETUP_UV}" in lockfile


def test_whenPackagingIsDebian_expectSetupUvNotLocked(generate: Generate) -> None:
    lockfile = read_lockfile(generate(packaging="debian-jammy-arm64"))

    assert SETUP_UV not in lockfile
