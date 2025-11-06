from typing import ClassVar

from ...core.activity import Activity


class Accept(Activity):
    AS_URI: ClassVar[str] = "https://www.w3.org/ns/activitystreams#Accept"


class TentativeAccept(Accept):
    AS_URI: ClassVar[str] = "https://www.w3.org/ns/activitystreams#TentativeAccept"
