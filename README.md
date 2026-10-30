# Template

Skip the setup. Start building. 🚀

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/downloads/)

Generate Python projects with the setup already done. Add your code and ship as a Python package, Debian package, or Docker image.

Every project comes with [uv](https://docs.astral.sh/uv/) for environment and dependency management, plus tools for linting, formatting, type checking, and testing.

[Choose how to ship](#choosing-a-packaging-option) or [create your first project](#generate-a-project).

## Choosing a packaging option

Three ways to ship. Pick the one that fits your project:

<details>
<summary><b>Python package</b>: the simplest option</summary>

<br>

**What it is:** a regular Python project, built as a source distribution and a wheel, and installed with `uv`, which sets up an isolated environment for you.

**Good for:** libraries, developer tools, and applications running somewhere you control and where Python or `uv` is available.

**Good to know:**

- The application still runs on a Python interpreter. `uv` can install a compatible one on the target, which needs internet access unless Python is already there.
- Dependencies are downloaded at install time, from PyPI, a private index, or a local folder of wheels. That last option also works offline.
- Packages with native code may need extra system libraries.

</details>

<details>
<summary><b>[WIP] Debian package (.deb)</b>: installs like any other app on Debian and Ubuntu</summary>

<br>

**What it is:** your application is bundled with its own Python and libraries (using [PyInstaller](https://pyinstaller.org/)), then packaged as a `.deb` with `debuild`.

**Good for:** Debian-based machines where you want the usual install, upgrade, and removal through APT, without worrying about which Python version is installed. What you learn here also applies to packaging non-Python applications.

**Benefits:**

- The target needs little beyond glibc (the standard C library), so the package can be installed without internet access, as long as any system dependencies are already there or supplied offline.
- You can use libraries that the distribution does not offer, or only offers in older versions.
- Each application brings its own libraries, so applications do not clash over dependency versions.
- It integrates with the system: install systemd service files, run setup and cleanup scripts on install and removal, and react to other packages through triggers.

**Good to know:**

- Build on the oldest Linux version you plan to support, and test on the real target systems.
- APT does not manage the bundled libraries: to ship an update for one of them, rebuild and redistribute the application.

</details>

<details>
<summary><b>[WIP] Docker image</b>: everything in one image</summary>

<br>

**What it is:** your application and the libraries it needs, packaged into a Docker image.

**Good for:** consistent deployments, and projects that rely on low-level or vendor-specific libraries that are hard to install or to package properly as a `.deb`.

**Good to know:**

- An image does not include hardware drivers; the host still needs them. For example, NVIDIA containers need a suitable NVIDIA driver on the host.
- The target needs a container runtime such as Docker Engine, which is not always available or wanted.
- The first download is usually heavier than a `.deb`, which can be painful over a mobile connection. Shared layers make later downloads smaller.

</details>

## Generate a project

With [Cookiecutter installed](https://cookiecutter.readthedocs.io/), run:

```sh
cookiecutter https://github.com/pywright/template
```

Answer the prompts, open the generated directory, and follow its README to start building.

## Contributing

Bug fixes, new features, and clearer docs are all welcome.

1. Fork the repository and create a branch.
2. Make your changes and add or update tests where needed.
3. Run the relevant checks listed by `make help`.
4. Open a pull request explaining what changed and why.

For larger changes, open an issue first to discuss your idea. Keep changes focused and update the documentation where needed.

## License

Licensed under the [MIT License](LICENSE).
