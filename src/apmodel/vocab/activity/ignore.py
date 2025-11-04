from pydantic import Field

from ...core.activity import Activity


class Ignore(Activity):
    type: str = Field(
        alias="@type",
        default="https://www.w3.org/ns/activitystreams#Ignore",
        kw_only=True,
    )