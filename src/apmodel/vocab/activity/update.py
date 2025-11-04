from pydantic import Field

from ...core.activity import Activity


class Update(Activity):
    type: str = Field(
        alias="@type",
        default="https://www.w3.org/ns/activitystreams#Update",
        kw_only=True,
    )