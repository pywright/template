import itertools
import json
from pathlib import Path
from typing import Protocol

COOKIECUTTER_JSON = Path(__file__).parent.parent / "cookiecutter.json"


class Generate(Protocol):
    def __call__(self, **context: str) -> Path: ...


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
