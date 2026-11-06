import pytest

from tests.helpers import Render, deb_packagings


def test_whenDefaultsAreUsed_expectTitleAndDescriptionUnchanged(
    render: Render,
) -> None:
    context = render()

    assert context["__title"] == context["title"]
    assert context["__description"] == context["description"]


@pytest.mark.parametrize(
    ("title", "expected"),
    [
        ("Well-Known", "Well-Known"),
        ("  Extra   inner   spaces  ", "Extra inner spaces"),
        ("Tabs\tand\nnewlines", "Tabs and newlines"),
        ("Ends with dot.", "Ends with dot"),
        ("Dot after space .", "Dot after space"),
    ],
)
def test_whenTitleIsSet_expectNormalizedTitle(
    render: Render, title: str, expected: str
) -> None:
    assert render(title=title)["__title"] == expected


@pytest.mark.parametrize(
    ("description", "expected"),
    [
        ("Already ends.", "Already ends."),
        ("Ends with bang!", "Ends with bang!"),
        ("Ends with question?", "Ends with question?"),
        ("No terminal punctuation", "No terminal punctuation."),
        ("  Extra   inner   spaces  ", "Extra inner spaces."),
    ],
)
def test_whenDescriptionIsSet_expectNormalizedDescription(
    render: Render, description: str, expected: str
) -> None:
    assert render(description=description)["__description"] == expected


@pytest.mark.parametrize(
    ("artifact", "expected"),
    [
        ("my-cool-app", "my_cool_app"),
        ("single", "single"),
        ("a-b-c", "a_b_c"),
    ],
)
def test_whenArtifactIsSet_expectModuleWithUnderscores(
    render: Render, artifact: str, expected: str
) -> None:
    assert render(artifact=artifact)["__module"] == expected


def test_whenGitConfigIsSet_expectAuthorAndEmailFromGit(render: Render) -> None:
    context = render()

    assert context["__author"] == "Jane Doe"
    assert context["__email"] == "jane.doe@example.com"


@pytest.mark.parametrize(
    ("packaging", "kind", "codename", "arch"),
    [
        ("debian-jammy-amd64", "debian", "jammy", "amd64"),
        ("debian-resolute-arm64", "debian", "resolute", "arm64"),
        ("python", "python", "", ""),
    ],
)
def test_whenPackagingIsSet_expectPackagingCodenameAndArch(
    render: Render, packaging: str, kind: str, codename: str, arch: str
) -> None:
    context = render(packaging=packaging)

    assert context["__packaging"] == kind
    assert context["__codename"] == codename
    assert context["__arch"] == arch


@pytest.mark.parametrize("packaging", deb_packagings())
def test_whenPackagingIsDeb_expectCodenameAndArchFromChoice(
    render: Render, packaging: str
) -> None:
    context = render(packaging=packaging)

    assert context["__packaging"] == "debian"
    assert packaging == f"debian-{context['__codename']}-{context['__arch']}"


@pytest.mark.parametrize(
    ("packaging", "expected"),
    [
        ("debian-jammy-amd64", "4.6.0"),
        ("debian-noble-arm64", "4.7.0"),
        ("debian-resolute-amd64", "4.7.4"),
        ("python", ""),
    ],
)
def test_whenPackagingIsSet_expectStandardsVersion(
    render: Render, packaging: str, expected: str
) -> None:
    assert render(packaging=packaging)["__standards"] == expected


@pytest.mark.parametrize("packaging", deb_packagings())
def test_whenPackagingIsDeb_expectEveryCodenameHasStandards(
    render: Render, packaging: str
) -> None:
    assert render(packaging=packaging)["__standards"]
