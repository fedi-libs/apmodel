from typing import Optional


from ...core.activity import Activity


class Flag(Activity):
    type: Optional[str] = "Flag"
