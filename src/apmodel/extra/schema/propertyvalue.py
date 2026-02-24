from typing import Optional

from pydantic import Field

from ...types import ActivityPubModel


class PropertyValue(ActivityPubModel):
    type: str = Field(default="PropertyValue", kw_only=True)

    name: Optional[str] = Field(default=None)
    value: Optional[str] = Field(default=None)
