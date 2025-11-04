from pydantic import Field

from ...core.activity import Activity


class Invite(Activity):
    type: str = Field(
        alias="@type",
        default="https://www.w3.org/ns/activitystreams#Invite",
        kw_only=True,
    )