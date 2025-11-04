from pydantic import Field

from ...core.activity import Activity


class Arrive(Activity):
    type: str = Field(
        alias="@type",
        default="https://www.w3.org/ns/activitystreams#Arrive",
        kw_only=True,
    )
