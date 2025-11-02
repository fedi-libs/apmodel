from typing import Annotated, Optional

from pydantic import BeforeValidator, Field

from ..core import Link
from ..helpers import get_value_from_array


class Hashtag(Link):
    type: Annotated[Optional[str], BeforeValidator(get_value_from_array)] = (
        Field(
            alias="@type",
            default="https://www.w3.org/ns/activitystreams#Hashtag",
            kw_only=True,
        )
    )
