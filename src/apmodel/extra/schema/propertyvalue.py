from pydantic import Field

from apmodel.types.aliases import OPT_STR

from ...types import ActivityPubModel


class PropertyValue(ActivityPubModel):
    type: str = Field(
        default="https://schema.org#PropertyValue",
        kw_only=True,
        alias="@type",
    )

    name: OPT_STR = Field(default=None)
    value: OPT_STR = Field(default=None)
