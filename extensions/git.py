import subprocess
import sys

from jinja2 import Environment
from jinja2.ext import Extension


def git_config(field: str) -> str:
    try:
        result = subprocess.run(
            ["git", "config", "--get", field],
            capture_output=True,
            text=True,
            check=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        sys.exit(
            f"Could not read git config '{field}'. Is git installed and the value set?"
        )
    return result.stdout.strip()


class GitExtension(Extension):
    """Expose `git_config()` to cookiecutter templates."""

    def __init__(self, environment: Environment) -> None:
        super().__init__(environment)
        environment.globals["git_config"] = git_config  # pyrefly: ignore[unsupported-operation]
