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

TASK_SCRIPT_ROOT = Path(__file__).parents[1]
REPO_ROOT = TASK_SCRIPT_ROOT.parent


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
            ],
            check=True,
        )

        requirements_path = TASK_SCRIPT_ROOT.joinpath("requirements.txt")

        requirements_abs_path = tmp_requirements.read_text()

        # Replace the absolute path of demo-ssp-ids with a relative path
        # demo-ssp-ids @ file:///repos/ts-scientific-data-and-ai-cloud-pipeline-examples/examples/all-in-one-ids-task-script-protocol/task_script/dependencies/demo_ssp_ids-0.1.0-py3-none-any.whl ; python_version == "3.11" \

        abs_substring = str(TASK_SCRIPT_ROOT)
        lines = []
        for line in requirements_abs_path.splitlines():
            if line.startswith("demo-ssp-ids @ file") and abs_substring in line:
                line = (
                    "."
                    + (
                        line[line.index(abs_substring) :]
                        .removeprefix(abs_substring)
                        .split()[0]
                    )
                    + " \\"
                )
            lines.append(line)
        requirements_relative_path = "\n".join(lines)

        # Add the "--find-links" option complete the requirements.txt file
        # This tells pip to look in the 'dependencies' folder for anything it can't find on PyPI
        requirements_path.write_text(
            "--find-links dependencies\n" + requirements_relative_path
        )


if __name__ == "__main__":
    generate_requirements()
