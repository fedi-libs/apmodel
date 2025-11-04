from pydantic import Field

from ...core.activity import Activity


class Accept(Activity):
    type: str = Field(
        alias="@type",
        default="https://www.w3.org/ns/activitystreams#Accept",
        kw_only=True,
    )


class TentativeAccept(Accept):
    type: str = Field(
        alias="@type",
        default="https://www.w3.org/ns/activitystreams#TentativeAccept",
        kw_only=True,
    )
