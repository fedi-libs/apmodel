from typing import Optional


from ..core.link import Link


class Mention(Link):
    type: Optional[str] = "Mention"
