from pydantic import Field

from ...core.activity import Activity


class Delete(Activity):
    type: str = Field(
        alias="@type",
        default="https://www.w3.org/ns/activitystreams#Delete",
        kw_only=True,
    )
