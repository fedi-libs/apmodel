from pydantic import Field

from ...core.activity import Activity


class Read(Activity):
    type: str = Field(
        alias="@type",
        default="https://www.w3.org/ns/activitystreams#Read",
        kw_only=True,
    )