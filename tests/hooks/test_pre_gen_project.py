import pytest
from pytest_cookies.plugin import Cookies


def test_whenContextIsValid_expectProjectGenerated(cookies: Cookies) -> None:
    result = cookies.bake()

    assert result.exit_code == 0
    assert result.exception is None


@pytest.mark.parametrize("artifact", ["Foo_bar", "has space", "BAZ"])
def test_whenArtifactIsInvalid_expectGenerationAborted(
    cookies: Cookies, artifact: str
) -> None:
    result = cookies.bake(extra_context={"artifact": artifact})

    assert result.exit_code != 0
