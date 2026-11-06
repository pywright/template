from datetime import datetime
from pathlib import Path

import pytest

from tests.helpers import Generate, choices

LICENSES = {
    "MIT": "Expat",
    "Apache-2.0": "Apache-2.0",
    "BSD-2-Clause": "BSD-2-clause",
    "BSD-3-Clause": "BSD-3-clause",
}


def read_copyright(project: Path) -> list[str]:
    return (project / "debian/copyright").read_text().splitlines()


def test_whenLicenseChoicesAreListed_expectEveryChoiceIsCovered() -> None:
    assert set(LICENSES) == set(choices()["license"])


@pytest.mark.parametrize("license", LICENSES)
def test_whenLicenseIsSet_expectDebianShortNameRendered(
    generate: Generate, license: str
) -> None:
    lines = read_copyright(generate(packaging="debian-jammy-arm64", license=license))

    assert f"License: {LICENSES[license]}" in lines


def test_whenAuthorIsSet_expectCopyrightLineRendered(generate: Generate) -> None:
    lines = read_copyright(
        generate(
            packaging="debian-jammy-arm64",
            __author="Jane Doe",
            __email="jane.doe@example.com",
        )
    )

    assert f"Copyright: {datetime.now().year} Jane Doe <jane.doe@example.com>" in lines
