import shutil
import subprocess
import sys
from pathlib import Path

PACKAGING = "{{ cookiecutter.__packaging }}"

if PACKAGING != "debian":
    for path in ("debian",):
        shutil.rmtree(Path(path))

try:
    subprocess.run(["git", "init", "--quiet"], check=True)
except (FileNotFoundError, subprocess.CalledProcessError):
    sys.exit("Could not run 'git init'. Is git installed?")
