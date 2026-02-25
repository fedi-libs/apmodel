from typing import Optional


from ...core.activity import Activity


class Ignore(Activity):
    type: Optional[str] = "Ignore"
