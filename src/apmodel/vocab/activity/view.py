from typing import Optional


from ...core.activity import Activity


class View(Activity):
    type: Optional[str] = "View"
