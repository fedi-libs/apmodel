from typing import Literal, Optional

from pydantic import Field

from ..core.object import Object


class Event(Object):
    type: str = Field(default="Event", kw_only=True, frozen=True)


class Place(Object):
    type: str = Field(default="Place", kw_only=True, frozen=True)
    accuracy: Optional[float] = Field(default=None)
    altitude: Optional[float] = Field(default=None)
    latitude: Optional[float] = Field(default=None)
    longitude: Optional[float] = Field(default=None)
    radius: Optional[float] = Field(default=None)
    units: Optional[str | Literal["cm", "feet", "inches", "km", "m", "miles"]] = Field(
        default=None
    )
