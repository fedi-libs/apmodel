from typing import Annotated, Optional

from pydantic import BeforeValidator, Field

from apmodel.types.aliases import OPT_STR

from ..core import Link
from ..helpers import get_value_from_array


class Hashtag(Link):
    type: str = (
        Field(
            alias="@type",
            default="https://www.w3.org/ns/activitystreams#Hashtag",
            kw_only=True,
        )
    )
