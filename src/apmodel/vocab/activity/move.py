from typing import Optional


from ...core.activity import Activity


class Move(Activity):
    type: Optional[str] = "Move"
