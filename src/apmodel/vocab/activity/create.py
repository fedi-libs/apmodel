from pydantic import Field

from ...core.activity import Activity


class Create(Activity):
    type: str = Field(
        alias="@type",
        default="https://www.w3.org/ns/activitystreams#Create",
        kw_only=True,
    )
