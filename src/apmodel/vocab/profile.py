from typing import Optional

from pydantic import Field

from ..core.object import Object


class Profile(Object):
    type: Optional[str] = "Profile"
    describes: Optional[Object] = Field(default=None)
