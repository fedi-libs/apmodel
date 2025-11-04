from pydantic import Field

from ...core.activity import Activity


class Leave(Activity):
    type: str = Field(
        alias="@type",
        default="https://www.w3.org/ns/activitystreams#Leave",
        kw_only=True,
    )