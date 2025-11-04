from pydantic import Field

from ...core.activity import Activity


class View(Activity):
    type: str = Field(
        alias="@type",
        default="https://www.w3.org/ns/activitystreams#View",
        kw_only=True,
    )