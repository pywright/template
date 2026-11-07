# {{ cookiecutter.__title }}

{{ cookiecutter.__description }}

## Developing

Requires [uv](https://docs.astral.sh/uv/). Run `make help` to list all available commands.

## Packaging
{%- if cookiecutter.__packaging == 'python' %}

`make build` writes the source distribution and wheel to `dist/`. Install the
wheel with:

```sh
uv tool install dist/*.whl
```
{%- elif cookiecutter.__packaging == 'debian' %}

`make build` builds the `.deb` in a Docker image and writes it to `dist/`, next
to a `.sha256` file with its checksum. Install it with:

```sh
sudo apt install ./dist/*.deb
```

Requirements:

- [Docker](https://docs.docker.com/engine/install/), with your user in the [`docker` group](https://docs.docker.com/engine/install/linux-postinstall/)
- To build for another architecture than this machine: [buildx](https://github.com/docker/buildx) and [QEMU](https://docs.docker.com/build/building/multi-platform/)
{%- endif %}

## Releasing

Push a `v*` tag to create a GitHub release with the build output and an SBOM.
