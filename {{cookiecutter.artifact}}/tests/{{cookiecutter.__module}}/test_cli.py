from importlib.metadata import version

from {{cookiecutter.__module}} import cli


class TestCli:
    def test_whenHelpRequested_thenHelpDisplayed(self, runner):
        result = runner.invoke(cli.cli, ["--help"])
        assert result.exit_code == 0
        assert "Usage:" in result.output
        assert "Options:" in result.output
        assert not result.stderr

    def test_whenVersionRequested_thenVersionDisplayed(self, runner):
        expected = version("{{cookiecutter.artifact}}")
        result = runner.invoke(cli.cli, ["--version"])
        assert result.exit_code == 0
        assert expected in result.output
        assert not result.stderr
