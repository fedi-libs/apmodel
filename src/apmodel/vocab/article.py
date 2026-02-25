from typing import Optional


from ..core.object import Object


class Article(Object):
    type: Optional[str] = "Article"
