"""
This script creates a 'requirements.txt' file and 'dependencies/' directory.
'requirements.txt' is used by the task script build process in TDP to install Python
dependencies.
'dependencies/' contains a vendored copy of any privately hosted Python packages, so that
they are available for the task script build process which only has access to publicly
hosted PyPI packages.
"""

import subprocess
import tempfile
from pathlib import Path

TASK_SCRIPT_ROOT = Path(__file__).parents[2]


def generate_requirements() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a temporary requirements/constraints file containing credentials for
        # downloading privately hosted packages
        tmp_constraints = Path(tmpdir).joinpath("constraints.txt")
        subprocess.run(
            [
                "poetry",
                "export",
                "-f",
                "constraints.txt",
                "-o",
                str(tmp_constraints),
                "--with-credentials",
                "--without-hashes",
            ],
            check=True,
        )

        # Download privately hosted packages into `/dependencies` to vendor them into
        # the task script
        dependencies = TASK_SCRIPT_ROOT.joinpath("dependencies")
        dependencies.mkdir(exist_ok=True)
        subprocess.run(
            [
                "pip",
                "download",
                "--no-deps",
                "--dest",
                str(dependencies),
                "--constraint",
                str(tmp_constraints),
                "ts-ids-core",
                "ts-ids-components",
            ],
            check=True,
        )

        # Create requirements in the format to be uploaded with the task script
        tmp_requirements = Path(tmpdir).joinpath("requirements.txt")
        subprocess.run(
            [
                "poetry",
                "export",
                "-f",
                "requirements.txt",
                "-o",
                str(tmp_requirements),
                "--without-urls",
            ],
            check=True,
        )

        requirements_path = TASK_SCRIPT_ROOT.joinpath("requirements.txt")

        # Add the "--find-links" option complete the requirements.txt file
        # This tells pip to look in the 'dependencies' folder for anything it can't find on PyPI
        requirements_path.write_text(
            "--find-links dependencies\n" + tmp_requirements.read_text()
        )


if __name__ == "__main__":
    generate_requirements()
