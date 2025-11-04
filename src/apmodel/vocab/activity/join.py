from pydantic import Field

from ...core.activity import Activity


class Join(Activity):
    type: str = Field(
        alias="@type",
        default="https://www.w3.org/ns/activitystreams#Join",
        kw_only=True,
    )