from typing import Annotated, Optional

from pydantic import BeforeValidator, Field

from ..core import Object
from ..helpers import get_value_from_array


class Emoji(Object):
    type: Annotated[Optional[str], BeforeValidator(get_value_from_array)] = (
        Field(
            alias="@type",
            default="http://joinmastodon.org/ns#Emoji",
            kw_only=True,
        )
    )
