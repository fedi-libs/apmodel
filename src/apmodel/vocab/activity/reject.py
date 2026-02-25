from typing import Optional


from ...core.activity import Activity


class Reject(Activity):
    type: Optional[str] = "Reject"


class TentativeReject(Reject):
    type: Optional[str] = "TentativeReject"
