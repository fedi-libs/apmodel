from typing import ClassVar

from ...core.activity import Activity


class Like(Activity):
    AS_URI: ClassVar[str] = "https://www.w3.org/ns/activitystreams#Like"