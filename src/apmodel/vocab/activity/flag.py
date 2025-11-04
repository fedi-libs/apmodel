from pydantic import Field

from ...core.activity import Activity


class Flag(Activity):
    type: str = Field(
        alias="@type",
        default="https://www.w3.org/ns/activitystreams#Flag",
        kw_only=True,
    )