from typing import Optional


from ...core.activity import Activity


class Leave(Activity):
    type: Optional[str] = "Leave"
