"""
Entrypoint for task script
"""

from typing import Any, Dict

import simplejson as json
from demo_ssp_ids.schema import Model
from demo_ssp_task_script import parse
from typing_extensions import TypedDict

DEFAULT_IDS_FILE_CATEGORY = "IDS"


class InputDict(TypedDict):
    """Inputs from the pipeline"""

    input_file_pointer: str


def main(task_inputs: InputDict, context) -> Dict[str, Any]:
    """TODO: what does this task script do?"""
    # Process the inputs
    input_file_pointer = task_inputs.get("input_file_pointer")

    # Get default IDS category. Note task_inputs may have {"ids_file_category": None}
    ids_file_category = task_inputs.get("ids_file_category")
    if ids_file_category is None:
        ids_file_category = DEFAULT_IDS_FILE_CATEGORY

    if input_file_pointer is None:
        raise FileNotFoundError("Input file not provided. Terminating...")

    input_file_info = context.read_file(input_file_pointer)
    file_contents = input_file_info.get("body", b"")

    # Do the task
    ids = parse.parse_file(file_contents)
    ids_json = ids.model_dump()

    # Validate against the JSON Schema
    context.validate_ids(
        data=ids_json, namespace=Model.NAMESPACE, slug=Model.TYPE, version=Model.VERSION
    )

    # Save to datalake
    output = context.write_file(
        content=json.dumps(ids_json, ignore_nan=True).encode(),
        file_name="0.json",
        file_category=ids_file_category,  # remove if not needed. only required for `common` namespace RAW to IDS Task Scripts
    )

    # Return info to pipeline
    return output
