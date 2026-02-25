from typing import Optional


from ...core.activity import Activity


class Create(Activity):
    type: Optional[str] = "Create"
