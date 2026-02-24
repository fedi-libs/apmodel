from typing import Optional

from pydantic import Field

from ...core.activity import Activity


class Undo(Activity):
    type: str = Field(default="Undo", kw_only=True, frozen=True)
