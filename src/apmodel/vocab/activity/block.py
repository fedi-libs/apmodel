from pydantic import Field

from ...core.activity import Activity


class Block(Activity):
    type: str = Field(
        alias="@type",
        default="https://www.w3.org/ns/activitystreams#Block",
        kw_only=True,
    )
