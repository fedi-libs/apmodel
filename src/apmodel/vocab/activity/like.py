from pydantic import Field

from ...core.activity import Activity


class Like(Activity):
    type: str = Field(
        alias="@type",
        default="https://www.w3.org/ns/activitystreams#Like",
        kw_only=True,
    )