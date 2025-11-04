from pydantic import Field

from ...core.activity import Activity


class Remove(Activity):
    type: str = Field(
        alias="@type",
        default="https://www.w3.org/ns/activitystreams#Remove",
        kw_only=True,
    )