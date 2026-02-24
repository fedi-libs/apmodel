from typing import Optional

from pydantic import Field

from ..core.object import Object


class Note(Object):
    type: str = Field(default="Note", kw_only=True, frozen=True)
