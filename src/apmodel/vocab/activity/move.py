from pydantic import Field

from ...core.activity import Activity


class Move(Activity):
    type: str = Field(
        alias="@type",
        default="https://www.w3.org/ns/activitystreams#Move",
        kw_only=True,
    )