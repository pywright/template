from tests.helpers import Generate

PYTHON_VERSION = "3.11"


def test_whenPythonIsSet_expectItIsTheOnlyLine(generate: Generate) -> None:
    project = generate(__python=PYTHON_VERSION)

    lines = (project / ".python-version").read_text().splitlines()

    assert lines == [PYTHON_VERSION]
