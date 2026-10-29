import pytest

from tests.helpers import AUTHOR, EMAIL, Render


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

    assert context["__author"] == AUTHOR
    assert context["__email"] == EMAIL
