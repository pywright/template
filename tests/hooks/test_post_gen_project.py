import pytest
from pytest_cookies.plugin import Cookies

DEB_DIRECTORIES = ("debian",)


def test_whenProjectIsGenerated_expectGitRepositoryInitialized(
    cookies: Cookies,
) -> None:
    result = cookies.bake()

    assert result.project_path is not None
    assert (result.project_path / ".git").is_dir()


@pytest.mark.parametrize("directory", DEB_DIRECTORIES)
def test_whenPackagingIsPython_expectDebDirectoryRemoved(
    cookies: Cookies, directory: str
) -> None:
    result = cookies.bake(extra_context={"packaging": "python"})

    assert result.exception is None
    assert result.project_path is not None
    assert not (result.project_path / directory).exists()


@pytest.mark.parametrize("directory", DEB_DIRECTORIES)
def test_whenPackagingIsDeb_expectDebDirectoryKept(
    cookies: Cookies, directory: str
) -> None:
    result = cookies.bake(extra_context={"packaging": "debian-jammy-arm64"})

    assert result.exception is None
    assert result.project_path is not None
    assert (result.project_path / directory).is_dir()
