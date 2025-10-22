"""
Tests for the Task Script entrypoint, main.py.
"""

from pathlib import Path
from typing import Any, Dict
from unittest.mock import MagicMock

import jsonschema
import main
import pytest
import simplejson as json
from ids.demo_ssp_ids.schema import Model


def validate_ids_mock(data: Dict[str, Any], **kwargs: Any):
    jsonschema.validate(data, Model.model_json_schema())


@pytest.mark.parametrize(
    "input_file",
    ["example_file.txt"],
)
def test_main(snapshot, input_file):
    """Test the main function (as much as is possible)"""
    # Arrange

    base_path = Path(__file__).parents[3]
    file_path = base_path.joinpath("example-input").joinpath(input_file)
    file_bytes = file_path.read_bytes()

    snapshot.snapshot_dir = base_path.joinpath("example-output")

    task_input = main.InputDict(input_file_pointer="a-file-pointer")

    # Create a mock representing the parts of the `context` object needed for this task
    # https://developers.tetrascience.com/docs/context-api
    context_mock = MagicMock()

    context_mock.read_file.return_value = {"body": file_bytes}
    context_mock.get_file_name.return_value = input_file

    context_mock.write_file.side_effect = lambda **kwargs: kwargs
    context_mock.validate_ids.side_effect = validate_ids_mock

    # Act
    res = main.main(task_input, context_mock)

    # Assert
    context_mock.read_file.assert_called_once_with("a-file-pointer")
    context_mock.validate_ids.assert_called_once()

    ids_instance = json.loads(res["content"])
    snapshot.assert_match(
        json.dumps(ids_instance, ignore_nan=True, indent=2),
        input_file + ".json",
    )
