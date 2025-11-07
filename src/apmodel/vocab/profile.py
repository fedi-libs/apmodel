from typing import Annotated, ClassVar, Optional

from pydantic import PlainSerializer, BeforeValidator, Field

from apmodel.helpers import generate_aliases, get_value_from_array, to_jld

from ..core.object import Object


class Profile(Object):
    AS_URI: ClassVar[str] = "https://www.w3.org/ns/activitystreams#Profile"
    
    describes: Annotated[
        Optional[Object], BeforeValidator(get_value_from_array), PlainSerializer(to_jld())
    ] = Field(default=None, **generate_aliases("describes", "as2"))
