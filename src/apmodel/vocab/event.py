from typing import Annotated, ClassVar, Literal, Optional, Union

from pydantic import PlainSerializer, BeforeValidator, Field

from apmodel.helpers import generate_aliases, get_value_from_array, to_jld
from apmodel.types.aliases import OPT_FLOAT

from ..core.object import Object


class Event(Object):
    AS_URI: ClassVar[str] = "https://www.w3.org/ns/activitystreams#Event"


class Place(Object):
    AS_URI: ClassVar[str] = "https://www.w3.org/ns/activitystreams#Place"

    accuracy: OPT_FLOAT = Field(default=None, **generate_aliases("accuracy", "as2"))
    altitude: OPT_FLOAT = Field(default=None, **generate_aliases("altitude", "as2"))
    latitude: OPT_FLOAT = Field(default=None, **generate_aliases("latitude", "as2"))
    longitude: OPT_FLOAT = Field(default=None, **generate_aliases("longitude", "as2"))
    radius: OPT_FLOAT = Field(default=None, **generate_aliases("radius", "as2"))
    units: Annotated[Optional[
        Union[str, Literal["cm", "feet", "inches", "km", "m", "miles"]]
    ], BeforeValidator(get_value_from_array), PlainSerializer(to_jld())] = Field(default=None, **generate_aliases("units", "as2"))
