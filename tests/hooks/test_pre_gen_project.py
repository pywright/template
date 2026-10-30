import pytest
from pytest_cookies.plugin import Cookies


@pytest.mark.parametrize("artifact", ["my-project", "app2", "a-b-c"])
def test_whenArtifactIsValid_expectProjectGenerated(
    cookies: Cookies, artifact: str
) -> None:
    result = cookies.bake(extra_context={"artifact": artifact})

    assert result.exit_code == 0
    assert result.exception is None


@pytest.mark.parametrize(
    "artifact",
    ["Foo_bar", "has space", "BAZ", "1app", "-foo", "foo-", "foo--bar"],
)
def test_whenArtifactIsInvalid_expectGenerationAborted(
    cookies: Cookies, artifact: str
) -> None:
    result = cookies.bake(extra_context={"artifact": artifact})

    assert result.exit_code != 0
