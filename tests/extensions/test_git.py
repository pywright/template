from pathlib import Path

import pytest
from jinja2 import Environment

from extensions.git import GitExtension, git_config
from tests.helpers import AUTHOR, EMAIL


def test_whenKeyIsSet_expectValueReturned() -> None:
    assert git_config("user.name") == AUTHOR
    assert git_config("user.email") == EMAIL


def test_whenKeyIsUnset_expectExitWithMessage() -> None:
    with pytest.raises(SystemExit, match="user.missing"):
        git_config("user.missing")


def test_whenGitIsMissing_expectExitWithMessage(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("PATH", str(tmp_path))  # empty dir, no git binary

    with pytest.raises(SystemExit, match="user.name"):
        git_config("user.name")


def test_whenExtensionIsLoaded_expectGitConfigAvailableInTemplates() -> None:
    env = Environment(extensions=[GitExtension])

    rendered = env.from_string("{{ git_config('user.email') }}").render()

    assert rendered == EMAIL
