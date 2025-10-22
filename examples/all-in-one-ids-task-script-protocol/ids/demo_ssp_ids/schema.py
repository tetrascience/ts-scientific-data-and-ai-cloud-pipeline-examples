from typing import ClassVar, List, Literal

from ts_ids_core.annotations import Required
from ts_ids_core.base.ids_field import IdsField
from ts_ids_core.schema import IdsSchema, SchemaExtraMetadataType, User


class Model(IdsSchema):
    NAMESPACE: ClassVar[str] = "private-{YOUR_ORG_SLUG}"
    TYPE: ClassVar[str] = "{YOUR_SLUG_PREFIX}demo-ssp"
    VERSION: ClassVar[str] = "v0.1.0"

    schema_extra_metadata: ClassVar[SchemaExtraMetadataType] = {
        "$id": f"https://ids.tetrascience.com/{NAMESPACE}/{TYPE}/{VERSION}/schema.json",
        "$schema": "http://json-schema.org/draft-07/schema",
    }

    ids_type: Required[Literal[TYPE]] = IdsField(
        default=TYPE,
        alias="@idsType",
    )
    ids_version: Required[Literal[VERSION]] = IdsField(
        default=VERSION,
        alias="@idsVersion",
    )
    ids_namespace: Required[Literal[NAMESPACE]] = IdsField(
        default=NAMESPACE,
        alias="@idsNamespace",
    )

    # Example of using the "users" component
    users: List[User] = IdsField(description="Users which produced the input data")

    file: str = IdsField(description="The entire raw file as a string")
