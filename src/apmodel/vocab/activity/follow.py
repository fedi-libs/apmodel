from typing import Optional


from ...core.activity import Activity


class Follow(Activity):
    type: Optional[str] = "Follow"
