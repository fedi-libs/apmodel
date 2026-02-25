from typing import Optional


from ...core.activity import IntransitiveActivity


class Arrive(IntransitiveActivity):
    type: Optional[str] = "Arrive"
