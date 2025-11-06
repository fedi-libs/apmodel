from typing import ClassVar

from pydantic import Field

from apmodel.types.aliases import OPT_STR

from ...types import ActivityPubModel


class PropertyValue(ActivityPubModel):
    AS_URI: ClassVar[str] = "https://schema.org#PropertyValue"

    name: OPT_STR = Field(default=None)
    value: OPT_STR = Field(default=None)