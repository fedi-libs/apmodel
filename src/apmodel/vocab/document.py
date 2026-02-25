from typing import Optional


from ..core.object import Object


class Document(Object):
    type: Optional[str] = "Document"


class Audio(Document):
    type: Optional[str] = "Audio"


class Image(Document):
    type: Optional[str] = "Image"


class Video(Document):
    type: Optional[str] = "Video"


class Page(Document):
    type: Optional[str] = "Page"
