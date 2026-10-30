"""{{ cookiecutter.__title }}."""

import logging
from importlib.metadata import version
from pathlib import Path

import click


class LogFormatter(logging.Formatter):
    """Custom logging formatter."""

    _MAX_FOLDERS = 3
    _LINE = "%(pathname)s::%(funcName)s:%(lineno)d"
    _FMT = f"%(name)s - %(levelname)s - {_LINE} - %(message)s"
    _FMT_TTY = f"%(asctime)s - {_FMT}"
    _DATEFMT = "%Y-%m-%dT%H:%M:%S"

    def __init__(self, tty: bool) -> None:
        super().__init__(self._FMT_TTY if tty else self._FMT, datefmt=self._DATEFMT)

    def format(self, record: logging.LogRecord) -> str:
        parts = Path(record.pathname).parts[-self._MAX_FOLDERS :]
        record.pathname = str(Path(*parts))
        return super().format(record)


def configure_logger(level: int) -> None:
    """Configure logging format."""
    handler = logging.StreamHandler()
    handler.setFormatter(LogFormatter(tty=handler.stream.isatty()))
    logging.basicConfig(level=level, handlers=[handler])


@click.command()
@click.option("-v", "--verbose", is_flag=True, help="Enables verbose mode.")
@click.version_option(version("{{ cookiecutter.artifact }}"))
def cli(verbose: bool) -> None:
    """Entry point for {{ cookiecutter.artifact }} CLI."""
    configure_logger(logging.DEBUG if verbose else logging.INFO)

    click.echo("{{ cookiecutter.artifact }} is ready.")


if __name__ == "__main__":
    cli()
