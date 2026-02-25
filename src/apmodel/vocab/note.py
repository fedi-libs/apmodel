from typing import Optional


from ..core.object import Object


class Note(Object):
    type: Optional[str] = "Note"
