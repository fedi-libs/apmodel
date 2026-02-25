from typing import Optional


from ...core.activity import Activity


class Remove(Activity):
    type: Optional[str] = "Remove"
