from typing import Optional


from ...core.activity import Activity


class Listen(Activity):
    type: Optional[str] = "Listen"
