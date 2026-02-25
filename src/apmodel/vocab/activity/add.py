from typing import Optional


from ...core.activity import Activity


class Add(Activity):
    type: Optional[str] = "Add"
