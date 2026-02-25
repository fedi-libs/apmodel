from typing import Optional


from ...core.activity import Activity


class Read(Activity):
    type: Optional[str] = "Read"
