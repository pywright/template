# Image for development and packaging.

ARG CODENAME
ARG UV_VERSION=0.13.6

FROM ghcr.io/astral-sh/uv:${UV_VERSION} AS uv

FROM ubuntu:${CODENAME}

ARG DEBIAN_FRONTEND=noninteractive

# Install system packages and the Build-Depends from debian/control
COPY debian/control /tmp/build-deps/debian/control
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        devscripts \
        fakeroot \
        git \
    && apt-get build-dep -y --no-install-recommends /tmp/build-deps \
    && rm -rf /var/lib/apt/lists/* /tmp/build-deps

# Copy the uv binaries from the official uv image
COPY --from=uv /uv /uvx /usr/local/bin/

# PyInstaller needs the shared library, which the system Python does not ship.
ENV UV_PYTHON_PREFERENCE=only-managed

# Run as ubuntu with the host UID and GID, so the mounted project stays writable.
ARG USER_UID=1000
ARG USER_GID=1000
{%- if cookiecutter.__codename == 'jammy' %}
RUN groupadd -o -g "$USER_GID" ubuntu \
    && useradd -o -m -u "$USER_UID" -g "$USER_GID" -s /bin/bash ubuntu
{%- else %}
RUN groupmod -o -g "$USER_GID" ubuntu \
    && usermod -o -u "$USER_UID" -g "$USER_GID" ubuntu
{%- endif %}

USER ubuntu

WORKDIR /home/ubuntu/app
