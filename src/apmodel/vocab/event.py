from typing import Annotated, Literal, Optional, Union

from pydantic import BeforeValidator, Field

from apmodel.helpers import get_value_from_array
from apmodel.types.aliases import OPT_FLOAT

from ..core.object import Object


class Event(Object):
    type: str = Field(
        default="https://www.w3.org/ns/activitystreams#Event",
        kw_only=True,
        alias="@type",
    )


class Place(Object):
    type: str = Field(
        default="https://www.w3.org/ns/activitystreams#Place",
        kw_only=True,
        alias="@type",
    )
    accuracy: OPT_FLOAT = Field(default=None)
    altitude: OPT_FLOAT = Field(default=None)
    latitude: OPT_FLOAT = Field(default=None)
    longitude: OPT_FLOAT = Field(default=None)
    radius: OPT_FLOAT = Field(default=None)
    units: Annotated[Optional[
        Union[str, Literal["cm", "feet", "inches", "km", "m", "miles"]]
    ], BeforeValidator(get_value_from_array)] = Field(default=None)
