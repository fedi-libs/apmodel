from typing import ClassVar

from ...core.activity import Activity


class Reject(Activity):
    AS_URI: ClassVar[str] = "https://www.w3.org/ns/activitystreams#Reject"


class TentativeReject(Reject):
    AS_URI: ClassVar[str] = "https://www.w3.org/ns/activitystreams#TentativeReject"
