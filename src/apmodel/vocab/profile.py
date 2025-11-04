from typing import Annotated, Optional

from pydantic import BeforeValidator, Field

from apmodel.helpers import get_value_from_array

from ..core.object import Object


class Profile(Object):
    type: str = Field(
        default="https://www.w3.org/ns/activitystreams#Profile",
        kw_only=True,
        alias="@type",
    )
    describes: Annotated[
        Optional[Object], BeforeValidator(get_value_from_array)
    ] = Field(default=None)
