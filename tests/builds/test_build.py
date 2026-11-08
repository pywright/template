import functools
import os
import platform
import subprocess
from pathlib import Path

import docker
import pytest

from tests.helpers import Generate, Render, case_id, variants

TIMEOUT_S = 1800
BUILDX_PATH = "/usr/local/libexec/docker/cli-plugins/docker-buildx"
HOST_ARCH = {"x86_64": "amd64", "aarch64": "arm64"}[platform.machine()]


@functools.cache
def install_qemu() -> None:
    """Register binfmt handlers so the host can run foreign-arch binaries."""
    docker.from_env(timeout=TIMEOUT_S).containers.run(
        "tonistiigi/binfmt",
        "--install arm64,amd64",
        privileged=True,
        remove=True,
    )


@functools.cache
def docker_config(base: Path) -> Path:
    """Give the Docker CLI buildx, to build for any architecture."""
    client = docker.from_env(timeout=TIMEOUT_S)

    # Copy the plugin out of the official docker:cli image.
    config = base / "docker"
    plugins = config / "cli-plugins"
    plugins.mkdir(parents=True)
    client.containers.run(
        "docker:cli",
        f"{BUILDX_PATH} /plugins",
        entrypoint="cp",
        user=f"{os.getuid()}:{os.getgid()}",
        volumes=[f"{plugins}:/plugins"],
        remove=True,
    )

    return config


def debian_variables(
    context: dict[str, str], arch: str, tmp_path_factory: pytest.TempPathFactory
) -> list[str]:
    """Make variables that isolate a Debian build from the host."""
    # Emulate only builds for another architecture.
    if arch != HOST_ARCH:
        install_qemu()

    base = tmp_path_factory.getbasetemp()
    return [
        # Stay out of the home and image of any real project with the same name.
        f"CONTAINER_HOME={base / context['packaging']}",
        f"IMAGE=template-build-test:{context['packaging']}",
        f"DOCKER_CONFIG={docker_config(base)}",
    ]


@pytest.mark.build
@pytest.mark.parametrize("context", variants(), ids=case_id)
def test_whenAnyParametersAreChosen_expectBuildPasses(
    generate: Generate,
    render: Render,
    context: dict[str, str],
    tmp_path_factory: pytest.TempPathFactory,
) -> None:
    project = generate(**context)
    # pre-commit only checks tracked files.
    subprocess.run(["git", "add", "."], cwd=project, check=True, capture_output=True)

    variables = []
    rendered = render(**context)
    if rendered["__packaging"] == "debian":
        variables = debian_variables(context, rendered["__arch"], tmp_path_factory)

    result = subprocess.run(
        ["make", "build", *variables],
        cwd=project,
        capture_output=True,
        text=True,
        timeout=TIMEOUT_S,
    )

    assert result.returncode == 0, result.stdout + result.stderr
