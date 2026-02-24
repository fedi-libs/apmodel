from typing import Optional

from pydantic import Field

from ..core.object import Object


class Profile(Object[str | None]):
    type: str = Field(default="Profile", kw_only=True, frozen=True)
    describes: Optional[Object] = Field(default=None)
