from pytest_cookies.plugin import Cookies


def test_whenProjectIsGenerated_expectGitRepositoryInitialized(
    cookies: Cookies,
) -> None:
    result = cookies.bake()

    assert (result.project_path / ".git").is_dir()
