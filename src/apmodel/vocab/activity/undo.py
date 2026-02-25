from typing import Optional


from ...core.activity import Activity


class Undo(Activity):
    type: Optional[str] = "Undo"
