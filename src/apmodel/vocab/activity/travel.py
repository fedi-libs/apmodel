from typing import ClassVar

from ...core.activity import Activity


class Travel(Activity):
    AS_URI: ClassVar[str] = "https://www.w3.org/ns/activitystreams#Travel"
