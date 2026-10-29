import itertools
import json
from pathlib import Path
from typing import Any, Protocol

COOKIECUTTER_JSON = Path(__file__).parent.parent / "cookiecutter.json"

# Identity returned by the isolated git config (see the `gitconfig` fixture).
AUTHOR = "Jane Doe"
EMAIL = "jane.doe@example.com"


class Generate(Protocol):
    def __call__(self, **context: str) -> Path: ...


class Render(Protocol):
    def __call__(self, **context: str) -> dict[str, Any]: ...


def choices() -> dict[str, list[str]]:
    """Public choice variables in cookiecutter.json, mapped to their options."""
    variables = json.loads(COOKIECUTTER_JSON.read_text())
    return {
        name: value
        for name, value in variables.items()
        if isinstance(value, list) and not name.startswith("_")
    }


def matrix() -> list[dict[str, str]]:
    """Every combination of the choice variables."""
    options = choices()
    return [
        dict(zip(options, combination, strict=True))
        for combination in itertools.product(*options.values())
    ]


def case_id(context: dict[str, str]) -> str:
    """Readable pytest id for one `matrix()` combination."""
    return "-".join(context.values())
