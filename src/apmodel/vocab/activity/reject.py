from pydantic import Field

from ...core.activity import Activity


class Reject(Activity):
    type: str = Field(
        alias="@type",
        default="https://www.w3.org/ns/activitystreams#Reject",
        kw_only=True,
    )


class TentativeReject(Reject):
    type: str = Field(
        alias="@type",
        default="https://www.w3.org/ns/activitystreams#TentativeReject",
        kw_only=True,
    )
