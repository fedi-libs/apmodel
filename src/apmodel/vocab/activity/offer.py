from pydantic import Field

from ...core.activity import Activity


class Offer(Activity):
    type: str = Field(
        alias="@type",
        default="https://www.w3.org/ns/activitystreams#Offer",
        kw_only=True,
    )