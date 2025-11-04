from pydantic import Field

from ...core.activity import Activity


class Announce(Activity):
    type: str = Field(
        alias="@type",
        default="https://www.w3.org/ns/activitystreams#Announce",
        kw_only=True,
    )
