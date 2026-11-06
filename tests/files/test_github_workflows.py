from pathlib import Path

import pytest

from tests.helpers import Generate, Render, deb_packagings

# __arch -> GitHub runner that builds natively for it
RUNNERS = {"amd64": "ubuntu-24.04", "arm64": "ubuntu-24.04-arm"}


def read_ci(project: Path) -> str:
    return (project / ".github" / "workflows" / "ci.yml").read_text()


@pytest.mark.parametrize("packaging", ["python", "debian-jammy-arm64"])
def test_whenPackagingIsSet_expectCiJobRunsMakeBuild(
    generate: Generate, packaging: str
) -> None:
    content = read_ci(generate(packaging=packaging))

    assert "  ci:\n" in content
    assert "        run: make build\n" in content


def test_whenPackagingIsPython_expectNoDebSteps(generate: Generate) -> None:
    content = read_ci(generate(packaging="python"))

    assert "deb" not in content


@pytest.mark.parametrize("packaging", deb_packagings())
def test_whenPackagingIsDeb_expectCiJobRunsOnNativeRunner(
    generate: Generate, render: Render, packaging: str
) -> None:
    content = read_ci(generate(packaging=packaging))

    runner = RUNNERS[render(packaging=packaging)["__arch"]]
    assert f"  ci:\n    runs-on: {runner}\n" in content


def test_whenCodenameAndArchAreSet_expectPackageAndChecksumUploaded(
    generate: Generate,
) -> None:
    content = read_ci(
        generate(
            packaging="debian-jammy-arm64",
            __codename="distinctive-codename",
            __arch="distinctive-arch",
            __standards="distinctive-standards",
        )
    )

    assert "          name: deb-distinctive-codename-distinctive-arch\n" in content
    assert "            dist/*.deb\n" in content
    assert "            dist/*.deb.sha256\n" in content


def test_whenProjectIsGenerated_expectCiWorkflowTokenIsReadOnly(
    generate: Generate,
) -> None:
    content = read_ci(generate())

    assert "permissions:\n  contents: read\n" in content


def test_whenProjectIsGenerated_expectSbomWorkflowKeepsGithubTokenExpression(
    generate: Generate,
) -> None:
    project = generate()

    content = (project / ".github" / "workflows" / "sbom.yml").read_text()

    assert "GH_TOKEN: ${{ github.token }}" in content
