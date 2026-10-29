import subprocess
import sys

try:
    subprocess.run(["git", "init", "--quiet"], check=True)
except (FileNotFoundError, subprocess.CalledProcessError):
    sys.exit("Could not run 'git init'. Is git installed?")
