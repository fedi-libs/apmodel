from pydantic import Field

from ...core.activity import Activity


class Listen(Activity):
    type: str = Field(
        alias="@type",
        default="https://www.w3.org/ns/activitystreams#Listen",
        kw_only=True,
    )