from typing import Optional

from pydantic import Field

from ...core.activity import Activity


class View(Activity):
    type: str = Field(default="View", kw_only=True, frozen=True)
