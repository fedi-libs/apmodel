import datetime
from typing import Annotated, Optional, Union

from pydantic import BeforeValidator, Field

from apmodel.helpers import get_value_from_array
from apmodel.types.aliases import OPT_DATETIME

from ..core.object import Object

class Tombstone(Object):
    type: str = Field(
        default="https://www.w3.org/ns/activitystreams#Tombstone",
        kw_only=True,
        alias="@type",
    )
    formerType: Annotated[
        Optional[Union[str, Object]], BeforeValidator(get_value_from_array)
    ] = Field(default=None)
    deleted: OPT_DATETIME  = Field(default=None)