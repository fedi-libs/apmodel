from __future__ import annotations

from typing import ClassVar, List, Literal, Optional, Union, Any, Dict

import msgspec
from ..types import BaseModel

NodeinfoProtocol: TypeAlias = Literal[
    "activitypub",
    "buddycloud",
    "dfrn",
    "diaspora",
    "libertree",
    "ostatus",
    "pumpio",
    "tent",
    "xmpp",
    "zot",
]


NodeinfoInbound: TypeAlias = Literal[
    "atom1.0",
    "gnusocial",
    "imap",
    "pnut",
    "pop3",
    "pumpio",
    "rss2.0",
    "twitter",
]

NodeinfoOutbound: TypeAlias = Literal[
    "atom1.0",
    "gnusocial",
    "blogger",
    "diaspora",
    "buddycloud",
    "dreamwidth",
    "drupal",
    "facebook",
    "friendica",
    "google",
    "insanejournal",
    "libertree",
    "linkedin",
    "livejournal",
    "mediagoblin",
    "myspace",
    "pinterest",
    "pnut",
    "posterous",
    "pumpio",
    "redmatrix",
    "rss2.0",
    "smtp",
    "tent",
    "tumblr",
    "twitter",
    "wordpress",
    "xmpp",
]


class NodeinfoServices(BaseModel):
    inbound: List[NodeinfoInbound]
    outbound: List[NodeinfoOutbound]


class NodeinfoUsageUsers(BaseModel):
    total: Optional[int] = msgspec.field(default=None)
    active_half_year: Optional[int] = msgspec.field(default=None)
    active_month: Optional[int] = msgspec.field(default=None)


class NodeinfoUsage(BaseModel):
    users: NodeinfoUsageUsers
    local_posts: Optional[int] = msgspec.field(default=None)
    local_comments: Optional[int] = msgspec.field(default=None)


class NodeinfoSoftware(BaseModel):
    name: Optional[str] = msgspec.field(default=None)
    version: Optional[str] = msgspec.field(default=None)
    repository: Optional[str] = msgspec.field(default=None)
    homepage: Optional[str] = msgspec.field(default=None)


class Nodeinfo(BaseModel):
    version: Literal["2.0", "2.1"]
    software: NodeinfoSoftware
    protocols: List[Union[NodeinfoProtocol, str]]
    services: NodeinfoServices
    open_registrations: bool
    usage: NodeinfoUsage
    metadata: dict

    _DETECTION_KEYS: ClassVar[List[str]] = [
        "version",
        "software",
        "protocols",
        "services",
        "openRegistrations",
        "usage",
        "metadata",
    ]

    @classmethod
    def is_nodeinfo_data(cls, data: dict) -> bool:
        """
        Checks if the given dictionary data matches Nodeinfo detection criteria.
        """
        # Note: data might have camelCase keys from JSON
        return all(key in data for key in cls._DETECTION_KEYS)

    @classmethod
    def model_validate(cls: type[Nodeinfo], data: Any) -> Nodeinfo:
        instance = super().model_validate(data)
        if instance.version == "2.0":
            if instance.software.repository:
                instance.software.repository = None
            if instance.software.homepage:
                instance.software.homepage = None
        return instance

    def model_dump(self, mode: str = "json", **kwargs) -> Dict[str, Any]:
        data = super().model_dump(mode=mode, **kwargs)
        if data.get("version") == "2.0":
            if "software" in data:
                data["software"].pop("repository", None)
                data["software"].pop("homepage", None)
        return data
