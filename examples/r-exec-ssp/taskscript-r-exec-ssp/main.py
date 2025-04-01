"""
Entrypoint for task script
"""

from typing import Any, Dict

import rpy2.robjects as ro
from rpy2.robjects.vectors import ByteVector


def main(task_input: Dict, context) -> Any:
    """
    Takes the text in `task_input['script']` and evals it
    """
    script = task_input.get("script")
    if script is None:
        raise ValueError("No script provided to task")
    if not isinstance(script, str):
        raise ValueError("Provided script must be a string")

    # Get input file
    input_data = context.read_file(task_input["input_file"])["body"]
    r_byte_string = ByteVector(input_data)

    # Get input file name
    input_file_name = context.get_file_name(task_input["input_file"])
    ro.globalenv["input_file_name"] = input_file_name

    # Assign the data to the R environment
    ro.globalenv["input_data"] = r_byte_string

    # Using R scripts
    result = ro.r(script)

    # Loop through result data from R and write to data lake
    for filename, content in result.items():
        print(f"File name: {filename}")
        # Ensure the first element is a valid string
        if not isinstance(filename, str):
            raise ValueError("The first element of the ListVector must be a string.")
        # Ensure the second element is a StrVector
        if not isinstance(content, ro.vectors.ByteVector):
            print(type(content))
            raise ValueError(
                "The second element of the ListVector must be a ByteVector."
            )

        # Write the ByteVector content to the file
        context.write_file(
            content=bytes(content), file_name=filename, file_category="PROCESSED"
        )
        print(f"Binary data written to '{filename}' successfully.")
