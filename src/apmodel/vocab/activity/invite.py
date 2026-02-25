from typing import Optional


from .offer import Offer


class Invite(Offer):
    type: Optional[str] = "Invite"
