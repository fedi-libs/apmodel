from typing import Optional


from ...core.activity import Activity


class Update(Activity):
    type: Optional[str] = "Update"
