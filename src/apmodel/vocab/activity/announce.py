from typing import Optional


from ...core.activity import Activity


class Announce(Activity):
    type: Optional[str] = "Announce"
