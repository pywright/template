import itertools
import json
from pathlib import Path
from typing import Any, Protocol

COOKIECUTTER_JSON = Path(__file__).parent.parent / "cookiecutter.json"


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


def debian_packagings() -> list[str]:
    """Packaging choices that build a Debian package."""
    return [p for p in choices()["packaging"] if p.startswith("debian-")]


def matrix() -> list[dict[str, str]]:
    """Every combination of the choice variables."""
    options = choices()
    return [
        dict(zip(options, combination, strict=True))
        for combination in itertools.product(*options.values())
    ]


def variants() -> list[dict[str, str]]:
    """Every option of every choice variable at least once, as few cases as possible."""
    options = choices()
    count = max(len(values) for values in options.values())
    return [
        {name: values[i % len(values)] for name, values in options.items()}
        for i in range(count)
    ]


def case_id(context: dict[str, str]) -> str:
    """Readable pytest id for one `matrix()` or `variants()` case."""
    return "-".join(context.values())
