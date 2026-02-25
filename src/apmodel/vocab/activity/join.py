from typing import Optional


from ...core.activity import Activity


class Join(Activity):
    type: Optional[str] = "Join"
