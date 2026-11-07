from pathlib import Path

import pytest

from tests.helpers import Generate, Render, deb_packagings

# __arch -> GitHub runner that builds natively for it
RUNNERS = {"amd64": "ubuntu-24.04", "arm64": "ubuntu-24.04-arm"}


def read_workflow(project: Path, name: str) -> str:
    return (project / ".github" / "workflows" / name).read_text()


@pytest.mark.parametrize("packaging", ["python", "debian-jammy-arm64"])
def test_whenPackagingIsSet_expectCiJobRunsMakeBuild(
    generate: Generate, packaging: str
) -> None:
    content = read_workflow(generate(packaging=packaging), "ci.yml")

    assert "  ci:\n" in content
    assert "        run: make build\n" in content


def test_whenPackagingIsPython_expectNoDebSteps(generate: Generate) -> None:
    content = read_workflow(generate(packaging="python"), "ci.yml")

    assert "deb" not in content


@pytest.mark.parametrize("packaging", deb_packagings())
def test_whenPackagingIsDeb_expectCiJobRunsOnNativeRunner(
    generate: Generate, render: Render, packaging: str
) -> None:
    content = read_workflow(generate(packaging=packaging), "ci.yml")

    runner = RUNNERS[render(packaging=packaging)["__arch"]]
    assert f"  ci:\n    runs-on: {runner}\n" in content


def test_whenCodenameAndArchAreSet_expectPackageAndChecksumUploaded(
    generate: Generate,
) -> None:
    content = read_workflow(
        generate(
            packaging="debian-jammy-arm64",
            __codename="distinctive-codename",
            __arch="distinctive-arch",
            __standards="distinctive-standards",
        ),
        "ci.yml",
    )

    assert "          name: deb-distinctive-codename-distinctive-arch\n" in content
    assert "            dist/*.deb\n" in content
    assert "            dist/*.deb.sha256\n" in content


def test_whenPackagingIsPython_expectDistributionsUploaded(
    generate: Generate,
) -> None:
    content = read_workflow(generate(packaging="python"), "ci.yml")

    assert "          path: dist/*\n" in content


@pytest.mark.parametrize("workflow", ["ci.yml", "sbom.yml"])
def test_whenProjectIsGenerated_expectWorkflowCallableWithReadOnlyToken(
    generate: Generate, workflow: str
) -> None:
    content = read_workflow(generate(), workflow)

    assert "  workflow_call:\n" in content
    assert "contents: read\n" in content
    assert "contents: write" not in content


def test_whenProjectIsGenerated_expectReleaseCreatedOnVersionTags(
    generate: Generate,
) -> None:
    content = read_workflow(generate(), "release.yml")

    assert '      - "v*"\n' in content
    assert "GH_TOKEN: ${{ github.token }}" in content
    assert 'gh release create "$GITHUB_REF_NAME" dist/* ' in content
