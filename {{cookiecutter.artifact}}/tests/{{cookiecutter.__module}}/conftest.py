"""Configuration settings and shared fixtures for pytest test cases."""

import pytest
from click.testing import CliRunner


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()
