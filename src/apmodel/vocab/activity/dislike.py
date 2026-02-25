from typing import Optional


from ...core.activity import Activity


class Dislike(Activity):
    type: Optional[str] = "Dislike"
