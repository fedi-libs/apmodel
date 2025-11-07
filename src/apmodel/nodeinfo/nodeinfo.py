from __future__ import annotations

import sys
from typing import List, Literal, Optional

if sys.version_info >= (3, 11):
    from enum import StrEnum
else:
    from backports.strenum import StrEnum

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    model_validator,
)
from pydantic_core import PydanticCustomError


class NodeinfoProtocol(StrEnum):
    ACTIVITYPUB = "activitypub"
    BUDDYCLOUD = "buddycloud"
    DFRN = "dfrn"
    DIASPORA = "diaspora"
    LIBERTREE = "libertree"
    OSTATUS = "ostatus"
    PUMPIO = "pumpio"
    TENT = "tent"
    XMPP = "xmpp"
    ZOT = "zot"


class NodeinfoInbound(StrEnum):
    ATOM1_0 = "atom1.0"
    GNUSOCIAL = "gnusocial"
    IMAP = "imap"
    PNUT = "pnut"
    POP3 = "pop3"
    PUMPIO = "pumpio"
    RSS2_0 = "rss2.0"
    TWITTER = "twitter"


class NodeinfoOutbound(StrEnum):
    ATOM1_0 = "atom1.0"
    GNUSOCIAL = "gnusocial"
    BLOGGER = "blogger"
    DIASPORA = "diaspora"
    BUDDYCLOUD = "buddycloud"
    DREAMWIDTH = "dreamwidth"
    DRUPAL = "drupal"
    FACEBOOK = "facebook"
    FRIENDICA = "friendica"
    GOOGLE = "google"
    INSANEJOURNAL = "insanejournal"
    LIBERTREE = "libertree"
    LINKEDIN = "linkedin"
    LIVEJOURNAL = "livejournal"
    MEDIAGOBLIN = "mediagoblin"
    MYSPACE = "myspace"
    PINTEREST = "pinterest"
    PNUT = "pnut"
    POSTEROUS = "posterous"
    PUMPIO = "pumpio"
    REDMATRIX = "redmatrix"
    RSS2_0 = "rss2.0"
    SMTP = "smtp"
    TENT = "tent"
    TUMBLR = "tumblr"
    TWITTER = "twitter"
    WORDPRESS = "wordpress"
    XMPP = "xmpp"


class NodeinfoServices(BaseModel):
    inbound: List[NodeinfoInbound | str] = Field(kw_only=True)
    outbound: List[NodeinfoOutbound | str] = Field(kw_only=True)


class NodeinfoUsageUsers(BaseModel):
    total: int = Field()
    activeHalfyear: int = Field()
    activeMonth: int = Field()


class NodeinfoUsage(BaseModel):
    users: NodeinfoUsageUsers
    localPosts: Optional[int] = Field(default=None)
    localComments: Optional[int] = Field(default=None)


class NodeinfoSoftware(BaseModel):
    model_config = ConfigDict(regex_engine="rust-regex")

    name: str = Field(pattern=r"^[a-z0-9-]+$")
    version: str = Field()
    repository: Optional[str] = Field(default=None)
    homepage: Optional[str] = Field(default=None)


class Nodeinfo(BaseModel):
    version: Literal["2.0", "2.1"]
    software: NodeinfoSoftware
    protocols: List[NodeinfoProtocol | str]
    services: NodeinfoServices
    openRegistrations: bool
    usage: NodeinfoUsage
    metadata: dict

    _DETECTION_KEYS = [
        "version",
        "software",
        "protocols",
        "services",
        "openRegistrations",
        "usage",
        "metadata",
    ]

    @model_validator(mode="after")
    def validate_nodeinfo_value(self) -> "Nodeinfo":
        if self.version == "2.0":
            if self.software.repository or self.software.homepage:
                raise PydanticCustomError(
                    "invalid_field",
                    "nodeinfo 2.0 can't contain software.repository and software.homepage",
                )
        return self

    @classmethod
    def is_nodeinfo_data(cls, data: dict) -> bool:
        """Checks if the given dictionary data matches Nodeinfo detection criteria."""
        return all(key in data for key in cls._DETECTION_KEYS)
