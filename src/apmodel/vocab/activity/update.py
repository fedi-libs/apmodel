from typing import Optional

from pydantic import Field

from ...core.activity import Activity


class Update(Activity):
    type: str = Field(default="Update", kw_only=True, frozen=True)
