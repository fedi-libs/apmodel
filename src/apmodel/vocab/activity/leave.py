from typing import Optional

from pydantic import Field

from ...core.activity import Activity


class Leave(Activity):
    type: str = Field(default="Leave", kw_only=True, frozen=True)
