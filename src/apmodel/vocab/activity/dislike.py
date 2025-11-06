from typing import ClassVar

from ...core.activity import Activity


class Dislike(Activity):
    AS_URI: ClassVar[str] = "https://www.w3.org/ns/activitystreams#Dislike"
