"""Configuration settings and shared fixtures for pytest test cases."""

from pathlib import Path
from typing import Any

import pytest
from cookiecutter.generate import generate_context
from cookiecutter.prompt import prompt_for_config
from pytest_cookies.plugin import Cookies

from tests.helpers import AUTHOR, COOKIECUTTER_JSON, EMAIL, Generate, Render


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line(
        "markers", "build: slow tests that run `make build` on generated projects"
    )


@pytest.fixture(autouse=True)
def gitconfig(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    path = tmp_path / "gitconfig"
    path.write_text(f"[user]\n\tname = {AUTHOR}\n\temail = {EMAIL}\n")
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


@pytest.fixture
def render() -> Render:
    """Render the `cookiecutter.json` variables without generating any files."""

    def _render(**context: str) -> dict[str, Any]:
        raw = generate_context(
            context_file=str(COOKIECUTTER_JSON), extra_context=context
        )
        return prompt_for_config(raw, no_input=True)

    return _render
