from typing import Optional


from ...core.activity import Activity


class Offer(Activity):
    type: Optional[str] = "Offer"
