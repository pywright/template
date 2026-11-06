# {{ cookiecutter.__title }}

{{ cookiecutter.__description }}

## Developing

Requires [uv](https://docs.astral.sh/uv/). Run `make` for help.

## Packaging
{%- if cookiecutter.__packaging == 'python' %}

`make build` writes the source distribution and wheel to `dist/`.
{%- elif cookiecutter.__packaging == 'debian' %}

`make build` builds the `.deb` for Ubuntu {{ cookiecutter.__codename }}, {{ cookiecutter.__arch }} in a
Docker image and writes it to `dist/`, next to a `.sha256` file with its
checksum.

Requirements:

- [Docker](https://docs.docker.com/engine/install/), with your user in the
  [`docker` group](https://docs.docker.com/engine/install/linux-postinstall/)
- To build for another architecture than this machine:
  [buildx](https://github.com/docker/buildx) and
  [QEMU](https://docs.docker.com/build/building/multi-platform/)
{%- endif %}
