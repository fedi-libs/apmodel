from typing import Annotated, ClassVar, Optional, Union

from pydantic import BeforeValidator, Field

from apmodel.helpers import generate_aliases, get_value_from_array
from apmodel.types.aliases import OPT_DATETIME

from ..core.object import Object


class Tombstone(Object):
    AS_URI: ClassVar[str] = "https://www.w3.org/ns/activitystreams#Tombstone"

    formerType: Annotated[
        Optional[Union[str, Object]], BeforeValidator(get_value_from_array)
    ] = Field(default=None, **generate_aliases("formerType", "as2"))
    deleted: OPT_DATETIME = Field(default=None, **generate_aliases("deleted", "as2"))
