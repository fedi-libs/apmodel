from typing import Optional


from ...core.activity import IntransitiveActivity


class Travel(IntransitiveActivity):
    type: Optional[str] = "Travel"
