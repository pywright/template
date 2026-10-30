from datetime import datetime

import pytest

from tests.helpers import AUTHOR, Generate, choices

# license -> (first line, last line); guards against wrong or truncated text.
LICENSES = {
    "MIT": ("MIT License", "SOFTWARE."),
    "Apache-2.0": ("Apache License", "limitations under the License."),
    "BSD-2-Clause": (
        "BSD 2-Clause License",
        "OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.",
    ),
    "BSD-3-Clause": (
        "BSD 3-Clause License",
        "OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.",
    ),
}

# Licenses whose text carries a year and holder; the rest are used verbatim.
COPYRIGHT_LINES = {
    "MIT": "Copyright (c) {year} {author}",
    "BSD-2-Clause": "Copyright (c) {year}, {author}",
    "BSD-3-Clause": "Copyright (c) {year}, {author}",
}
VERBATIM = [name for name in LICENSES if name not in COPYRIGHT_LINES]


def test_whenLicenseChoicesAreListed_expectEveryChoiceIsCovered() -> None:
    assert set(LICENSES) == set(choices()["license"])


def test_whenLicenseIsNotSet_expectMitLicense(generate: Generate) -> None:
    text = (generate() / "LICENSE").read_text()

    assert text.strip().splitlines()[0] == LICENSES["MIT"][0]


@pytest.mark.parametrize("license", LICENSES)
def test_whenLicenseIsSet_expectOnlyThatLicenseFile(
    generate: Generate, license: str
) -> None:
    project = generate(license=license)
    first, last = LICENSES[license]

    lines = [line.strip() for line in (project / "LICENSE").read_text().splitlines()]
    lines = [line for line in lines if line]

    assert lines[0] == first
    assert lines[-1] == last
    assert [p.name for p in project.iterdir() if "LICENSE" in p.name.upper()] == [
        "LICENSE"
    ]


@pytest.mark.parametrize("license", COPYRIGHT_LINES)
def test_whenLicenseHasCopyrightLine_expectCurrentYearAndAuthor(
    generate: Generate, license: str
) -> None:
    project = generate(license=license, __author=AUTHOR)

    lines = [line.strip() for line in (project / "LICENSE").read_text().splitlines()]

    year = datetime.now().year
    assert COPYRIGHT_LINES[license].format(year=year, author=AUTHOR) in lines


@pytest.mark.parametrize("license", VERBATIM)
def test_whenLicenseIsVerbatim_expectAuthorNotInjected(
    generate: Generate, license: str
) -> None:
    text = (generate(license=license, __author=AUTHOR) / "LICENSE").read_text()

    assert AUTHOR not in text


@pytest.mark.parametrize("license", COPYRIGHT_LINES)
def test_whenLicenseIsSet_expectNoLeftoverPlaceholders(
    generate: Generate, license: str
) -> None:
    text = (generate(license=license) / "LICENSE").read_text()

    for placeholder in ("[year]", "[fullname]", "[yyyy]", "[name of copyright owner]"):
        assert placeholder not in text
