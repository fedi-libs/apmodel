from pydantic import Field

from ...core.activity import Activity


class Dislike(Activity):
    type: str = Field(
        alias="@type",
        default="https://www.w3.org/ns/activitystreams#Dislike",
        kw_only=True,
    )
