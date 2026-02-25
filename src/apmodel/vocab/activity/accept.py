from typing import Optional

from ...core.activity import Activity


class Accept(Activity):
    type: Optional[str] = "Accept"


class TentativeAccept(Accept):
    type: Optional[str] = "TentativeAccept"
