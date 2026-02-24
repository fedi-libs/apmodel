from typing import Optional

from pydantic import Field

from ..core.object import Object


class Document(Object):
    type: str = Field(default="Document", kw_only=True, frozen=True)


class Audio(Document):
    type: str = Field(default="Audio", kw_only=True, frozen=True)


class Image(Document):
    type: str = Field(default="Image", kw_only=True, frozen=True)


class Video(Document):
    type: str = Field(default="Video", kw_only=True, frozen=True)


class Page(Document):
    type: str = Field(default="Page", kw_only=True, frozen=True)
