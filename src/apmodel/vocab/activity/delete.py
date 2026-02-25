from typing import Optional


from ...core.activity import Activity


class Delete(Activity):
    type: Optional[str] = "Delete"
