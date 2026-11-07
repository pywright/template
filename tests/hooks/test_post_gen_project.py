import pytest
from pytest_cookies.plugin import Cookies

DEBIAN_DIRECTORIES = ("debian", "packaging")


def test_whenProjectIsGenerated_expectGitRepositoryInitialized(
    cookies: Cookies,
) -> None:
    result = cookies.bake()

    assert result.project_path is not None
    assert (result.project_path / ".git").is_dir()


@pytest.mark.parametrize("directory", DEBIAN_DIRECTORIES)
def test_whenPackagingIsPython_expectDebianDirectoryRemoved(
    cookies: Cookies, directory: str
) -> None:
    result = cookies.bake(extra_context={"packaging": "python"})

    assert result.exception is None
    assert result.project_path is not None
    assert not (result.project_path / directory).exists()


@pytest.mark.parametrize("directory", DEBIAN_DIRECTORIES)
def test_whenPackagingIsDebian_expectDebianDirectoryKept(
    cookies: Cookies, directory: str
) -> None:
    result = cookies.bake(extra_context={"packaging": "debian-jammy-arm64"})

    assert result.exception is None
    assert result.project_path is not None
    assert (result.project_path / directory).is_dir()
