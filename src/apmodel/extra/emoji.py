from typing import Annotated, Optional

from pydantic import BeforeValidator, Field

from apmodel.types.aliases import OPT_STR

from ..core import Object
from ..helpers import get_value_from_array


class Emoji(Object):
    type: str = (
        Field(
            alias="@type",
            default="http://joinmastodon.org/ns#Emoji",
            kw_only=True,
        )
    )
