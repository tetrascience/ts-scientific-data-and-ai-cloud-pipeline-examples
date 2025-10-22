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
import glob

REPO_ROOT = Path(__file__).parents[1]
TASK_SCRIPT_ROOT = REPO_ROOT.joinpath("task_script")


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
                "--project",
                str(TASK_SCRIPT_ROOT),
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

        ## Build demo_ssp_ids from repo_root/ids
        subprocess.run(
            [
                "poetry",
                "build",
                "-f",
                "wheel",
                "-o",
                str(dependencies),
                "--project",
                str(REPO_ROOT.joinpath("ids")),
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
                "--without-hashes",
                "--project",
                str(TASK_SCRIPT_ROOT),
            ],
            check=True,
        )

        requirements_path = TASK_SCRIPT_ROOT.joinpath("requirements.txt")

        ids_wheel_path = glob.glob(str(dependencies.joinpath("demo_ssp_ids*.whl")))[0]
        relative_ids_wheel_path = (
            Path(ids_wheel_path).relative_to(TASK_SCRIPT_ROOT).as_posix()
        )

        requirements_abs_path = tmp_requirements.read_text()

        # Replace the source of demo-ssp-ids with the wheel file (relative to the task_script folder)
        requirements_w_fixed_path = "\n".join(
            [
                line
                if not line.startswith("demo-ssp-ids")
                else f"file:{relative_ids_wheel_path}"
                for line in requirements_abs_path.splitlines()
            ]
        )

        # Add the "--find-links" option complete the requirements.txt file
        # This tells pip to look in the 'dependencies' folder for anything it can't find on PyPI
        requirements_path.write_text(
            "--find-links dependencies\n" + requirements_w_fixed_path
        )


if __name__ == "__main__":
    generate_requirements()
