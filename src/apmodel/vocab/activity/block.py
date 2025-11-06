from typing import ClassVar

from ...core.activity import Activity


class Block(Activity):
    AS_URI: ClassVar[str] = "https://www.w3.org/ns/activitystreams#Block"
