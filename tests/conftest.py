"""Configuration settings and shared fixtures for pytest test cases."""

from pathlib import Path

import pytest
from pytest_cookies.plugin import Cookies

from tests.helpers import Generate


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line(
        "markers", "build: slow tests that run `make build` on generated projects"
    )


@pytest.fixture(autouse=True)
def gitconfig(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    path = tmp_path / "gitconfig"
    path.write_text("[user]\n\tname = Jane Doe\n\temail = jane.doe@example.com\n")
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", str(path))
    monkeypatch.setenv("GIT_CONFIG_NOSYSTEM", "1")
    return path


@pytest.fixture
def generate(cookies: Cookies) -> Generate:
    def _generate(**context: str) -> Path:
        result = cookies.bake(extra_context=context)
        assert result.exception is None
        assert result.exit_code == 0
        assert result.project_path is not None
        return result.project_path

    return _generate
