from typing import Optional


from ...core.activity import Activity


class Like(Activity):
    type: Optional[str] = "Like"
