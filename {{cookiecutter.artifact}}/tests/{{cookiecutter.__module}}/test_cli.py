from importlib.metadata import version

from click.testing import CliRunner

from {{ cookiecutter.__module }} import cli


def test_whenHelpIsSet_expectUsageWritten(runner: CliRunner) -> None:
    # Act
    result = runner.invoke(cli.cli, ["--help"])

    # Assert
    assert result.exit_code == 0
    assert "Usage:" in result.output
    assert "Options:" in result.output
    assert not result.stderr


def test_whenVersionIsSet_expectVersionWritten(runner: CliRunner) -> None:
    # Prepare
    expected = version("{{ cookiecutter.artifact }}")

    # Act
    result = runner.invoke(cli.cli, ["--version"])

    # Assert
    assert result.exit_code == 0
    assert expected in result.output
    assert not result.stderr
