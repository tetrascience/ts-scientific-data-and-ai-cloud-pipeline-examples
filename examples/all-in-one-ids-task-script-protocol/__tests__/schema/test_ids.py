import json
from pathlib import Path

import pytest
from ids.expected import create_example
from ids.schema import Model
from ids_es_json_generator import create_elasticsearch
from ids_validator.ids_validator import validate_ids
from pytest_snapshot.plugin import Snapshot

IDS_FOLDER = Path(__file__).parents[2].joinpath("ids")


def test_json_schema(snapshot: Snapshot) -> None:
    """
    The content of `schema.json` is created as a snapshot of the JSON Schema exported
    from the programmatic IDS.
    When running pytest, this test if fail if the two are out of sync.

    `pytest --snapshot-update` can be used to update `schema.json`.
    """
    # Arrange
    snapshot.snapshot_dir = IDS_FOLDER
    schema_path = IDS_FOLDER.joinpath("schema.json")

    # Act
    schema_json = Model.schema_json(indent=2)

    # Assert
    snapshot.assert_match(schema_json, schema_path)


def test_expected(snapshot: Snapshot) -> None:
    """
    The content of `expected.json` should match what is output by
    `ids.expected.create_example`.
    """
    # Arrange
    snapshot.snapshot_dir = IDS_FOLDER
    expected_path = IDS_FOLDER.joinpath("expected.json")

    # Act
    expected = create_example()
    excepted_json = expected.model_dump_json(indent=2)

    # Assert
    snapshot.assert_match(excepted_json, expected_path)


def test_elasticsearch_mapping(snapshot: Snapshot) -> None:
    """
    A simple default Elasticsearch mapping can be created using the ts-ids-es-json-generator
    package.
    It takes every array of objects in the schema and makes it a 'nested' mapping,
    along with a few other defaults.

    After running `pytest --snapshot-update`, inspect the 'elasticsearch.json', this
    test can be removed if a custom mapping is preferred.
    """
    # Arrange
    snapshot.snapshot_dir = IDS_FOLDER
    elasticsearch_path = IDS_FOLDER.joinpath("elasticsearch.json")

    # Act
    elasticsearch_mapping = create_elasticsearch(Model.model_json_schema())

    # Assert
    snapshot.assert_match(
        json.dumps(elasticsearch_mapping, indent=2), elasticsearch_path
    )


def test_ids_artifact_validation(capsys: pytest.CaptureFixture):
    """
    The IDS artifact should pass `ts-ids-validator` validation which ensures it follows
    platform requirements.

    This validation also runs when uploading the IDS to TDP, but including it as a test
    creates a faster feedback loop if validation fails.
    """
    # Arrange and act
    result = validate_ids(IDS_FOLDER)

    # Capture the output of the IDS validator from STDOUT
    validator_output, _ = capsys.readouterr()

    # Assert
    assert result, f"IDS Validator failed, output:\n\n{validator_output}\n\n"
