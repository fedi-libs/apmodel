from typing import Optional

from ...vocab.activity.like import Like


class EmojiReact(Like, kw_only=True):
    content: Optional[str] = None