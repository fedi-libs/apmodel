from typing import Optional

from ...types import ActivityPubModel


class PropertyValue(ActivityPubModel):
    type: Optional[str] = "PropertyValue"

    name: Optional[str] = None
    value: Optional[str] = None
