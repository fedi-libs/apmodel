from pydantic import Field

from ...core.activity import Activity


class Travel(Activity):
    type: str = Field(
        alias="@type",
        default="https://www.w3.org/ns/activitystreams#Travel",
        kw_only=True,
    )