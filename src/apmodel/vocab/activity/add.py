from pydantic import Field

from ...core.activity import Activity


class Add(Activity):
    type: str = Field(
        alias="@type",
        default="https://www.w3.org/ns/activitystreams#Add",
        kw_only=True,
    )