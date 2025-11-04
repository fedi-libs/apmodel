from pydantic import Field

from ..core.link import Link


class Mention(Link):
    type: str = Field(
        default="https://www.w3.org/ns/activitystreams#Mention",
        kw_only=True,
        alias="@type",
    )
