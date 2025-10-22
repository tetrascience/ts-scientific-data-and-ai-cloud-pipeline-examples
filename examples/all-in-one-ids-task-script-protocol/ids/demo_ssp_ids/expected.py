"""An example of IDS instance data.

This is used to populate the `expected.json` file in the IDS.
"""

from demo_ssp_ids.schema import Model
from ts_ids_core.schema import User


def create_example() -> Model:
    """Create an example of IDS data."""
    return Model(users=[User(name="guest")], file="original_file_content")
