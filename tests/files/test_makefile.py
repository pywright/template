from pathlib import Path

import pytest

from tests.helpers import Generate


def read_makefile(project: Path) -> str:
    return (project / "Makefile").read_text()


def test_whenArtifactIsSet_expectArtifactVariableRendered(generate: Generate) -> None:
    lines = read_makefile(generate(artifact="distinctive-artifact")).splitlines()

    assert "ARTIFACT := distinctive-artifact" in lines


def test_whenCodenameAndArchAreSet_expectVariablesRendered(
    generate: Generate,
) -> None:
    lines = read_makefile(
        generate(
            packaging="debian-jammy-arm64",
            __codename="distinctive-codename",
            __arch="distinctive-arch",
            __standards="distinctive-standards",
        )
    ).splitlines()

    assert "CODENAME := distinctive-codename" in lines
    assert "ARCH ?= distinctive-arch" in lines


def test_whenModuleIsSet_expectModuleVariableRendered(generate: Generate) -> None:
    lines = read_makefile(
        generate(packaging="debian-jammy-arm64", __module="distinctive_module")
    ).splitlines()

    assert "MODULE := distinctive_module" in lines


@pytest.mark.parametrize("target", ["image", "shell", "pyinstaller", "pkg", "build"])
def test_whenPackagingIsDeb_expectTargetExists(generate: Generate, target: str) -> None:
    lines = read_makefile(generate(packaging="debian-jammy-arm64")).splitlines()

    assert any(line.startswith(f"{target}:") for line in lines)


def test_whenPackagingIsDeb_expectNoUvBuild(generate: Generate) -> None:
    text = read_makefile(generate(packaging="debian-jammy-arm64"))

    assert "uv build" not in text


def test_whenPackagingIsPython_expectBuildTargetRunsUvBuild(
    generate: Generate,
) -> None:
    lines = read_makefile(generate(packaging="python")).splitlines()

    assert "\tuv build" in lines


def test_whenPackagingIsPython_expectNoDebTarget(generate: Generate) -> None:
    text = read_makefile(generate(packaging="python"))

    assert "deb" not in text
    assert "CODENAME" not in text
