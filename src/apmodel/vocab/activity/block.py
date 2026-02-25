from typing import Optional


from .ignore import Ignore


class Block(Ignore):
    type: Optional[str] = "Block"
