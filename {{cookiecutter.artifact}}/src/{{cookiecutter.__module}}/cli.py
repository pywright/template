"""{{cookiecutter.__title}}."""

import logging
import os
import sys
from importlib.metadata import version

import click


class LogFormatter(logging.Formatter):
    """Custom logging formatter."""

    _MAX_FOLDERS = 3
    _LINE = "%(pathname)s::%(funcName)s:%(lineno)d"
    _FMT = f"%(name)s - %(levelname)s - {_LINE} - %(message)s"
    _FMT_TTY = f"%(asctime)s - {_FMT}"

    def __init__(self) -> None:
        super().__init__(self._FMT if not sys.stdout.isatty() else self._FMT_TTY)

    def format(self, record: logging.LogRecord) -> str:
        sections = record.pathname.split(os.path.sep)
        record.pathname = os.path.sep.join(sections[-self._MAX_FOLDERS :])
        return super().format(record)


def configure_logger(level: int) -> None:
    """Configure logging format."""
    logging.basicConfig(level=level, datefmt="%Y-%m-%dT%H:%M:%S")
    logging.getLogger().handlers[0].setFormatter(LogFormatter())


@click.command()
@click.option("-v", "--verbose", is_flag=True, help="Enables verbose mode.")
@click.version_option(version("{{cookiecutter.artifact}}"))
def cli(verbose: bool) -> None:
    """Entry point for {{cookiecutter.artifact}} CLI."""
    configure_logger(logging.DEBUG if verbose else logging.INFO)


if __name__ == "__main__":
    cli()
