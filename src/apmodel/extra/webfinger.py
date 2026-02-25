import re
from typing import Any, Dict, List, NamedTuple, Optional

import msgspec


class Resource(NamedTuple):
    username: str
    host: str
    url: Optional[str] = None

    def __str__(self) -> str:
        if self.url:
            return self.url
        return f"acct:{self.username}@{self.host}"

    @classmethod
    def parse(cls, resource_str: str) -> "Resource":
        if not resource_str:
            return cls(username="", host="", url="")

        _raw = resource_str
        clean_str = (
            resource_str[5:]
            if resource_str.startswith("acct:")
            else resource_str
        )
        match = re.match(r"^([^@]+)@([^@]+)$", clean_str)
        if not match:
            return cls(username="", host="", url=_raw)

        username, host = match.groups()
        return cls(username=username, host=host, url=None)

    def export(self) -> str:
        return str(self)


class Link(msgspec.Struct, frozen=True):
    rel: str
    type: Optional[str]
    href: Optional[str]

    def to_json(self) -> dict:
        return msgspec.to_builtins(self)


class Result(msgspec.Struct, frozen=True):
    subject: Resource
    links: List[Link]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Result":
        subject_str = data.get("subject")
        if not subject_str:
            raise ValueError("Missing 'subject'")

        subject = Resource.parse(subject_str)

        links = msgspec.convert(data.get("links", []), List[Link])

        return cls(subject=subject, links=links)

    def get(self, link_type: str) -> List[Link]:
        return [link for link in self.links if link.type == link_type]

    def to_json(self) -> dict:
        return {
            "subject": self.subject.export(),
            "links": [link.to_json() for link in self.links],
        }