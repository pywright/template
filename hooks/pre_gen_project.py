import re
import sys

ARTIFACT_PATTERN = r"^[a-z0-9-]+$"

artifact = "{{ cookiecutter.artifact }}"

if not re.fullmatch(ARTIFACT_PATTERN, artifact):
    sys.exit(
        f"Invalid artifact name '{artifact}': "
        "use only lowercase letters, digits and hyphens"
    )
