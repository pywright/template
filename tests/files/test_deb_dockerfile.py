from pathlib import Path

import pytest

from tests.helpers import Generate, deb_packagings

# Ubuntu images without an `ubuntu` user.
CODENAMES_WITHOUT_USER = {"jammy"}


def read_dockerfile(project: Path) -> str:
    return (project / "packaging/deb.Dockerfile").read_text()


def test_whenProjectIsGenerated_expectCodenameRequired(generate: Generate) -> None:
    lines = read_dockerfile(generate(packaging="debian-jammy-arm64")).splitlines()

    assert "ARG CODENAME" in lines
    assert "FROM ubuntu:${CODENAME}" in lines


def test_whenProjectIsGenerated_expectBuildDependsInstalledFromControl(
    generate: Generate,
) -> None:
    text = read_dockerfile(generate(packaging="debian-jammy-arm64"))

    assert "COPY debian/control /tmp/build-deps/debian/control\n" in text
    assert "apt-get build-dep -y --no-install-recommends /tmp/build-deps" in text


def test_whenProjectIsGenerated_expectBuildToolsInstalled(generate: Generate) -> None:
    lines = read_dockerfile(generate(packaging="debian-jammy-arm64")).splitlines()

    assert "        ca-certificates \\" in lines
    assert "        devscripts \\" in lines
    assert "        fakeroot \\" in lines
    assert "        git \\" in lines


@pytest.mark.parametrize("packaging", deb_packagings())
def test_whenCodenameIsSet_expectUbuntuUserMatchesImage(
    generate: Generate, packaging: str
) -> None:
    text = read_dockerfile(generate(packaging=packaging))

    create = '&& useradd -o -m -u "$USER_UID" -g "$USER_GID" -s /bin/bash ubuntu\n'
    modify = '&& usermod -o -u "$USER_UID" -g "$USER_GID" ubuntu\n'
    if packaging.split("-")[1] in CODENAMES_WITHOUT_USER:
        assert 'RUN groupadd -o -g "$USER_GID" ubuntu' in text
        assert create in text
        assert modify not in text
    else:
        assert 'RUN groupmod -o -g "$USER_GID" ubuntu' in text
        assert modify in text
        assert create not in text


def test_whenProjectIsGenerated_expectWorkInHomeAsUbuntu(generate: Generate) -> None:
    lines = read_dockerfile(generate(packaging="debian-jammy-arm64")).splitlines()

    assert "USER ubuntu" in lines
    assert "WORKDIR /home/ubuntu/app" in lines
