from __future__ import annotations

from typing import Any, Dict, List, TypeVar, Union

import msgspec

LDContextType = TypeVar("LDContextType", bound="LDContext")


class LDContext(msgspec.Struct):
    """
    Parses and manages a JSON-LD @context, ensuring uniqueness.

    - String URLs are stored in a list, with duplicates ignored.
    - Dictionary definitions are merged, with later values overwriting earlier
      ones for the same key.
    This provides a list-like interface to the full context.
    """

    urls: List[str] = msgspec.field(default_factory=list)
    definitions: Dict[str, Any] = msgspec.field(default_factory=dict)

    @classmethod
    def from_any(cls, context: Any) -> LDContext:
        instance = cls()
        if context is not None:
            instance.add(context)
        return instance

    def add(self, context: Any) -> None:
        if context is None:
            return

        if not isinstance(context, list):
            items = [context]
        else:
            items = context

        for item in items:
            if isinstance(item, str):
                if item not in self.urls:
                    self.urls.append(item)
            elif isinstance(item, dict):
                self.definitions.update(item)
            elif isinstance(item, LDContext):
                self.add(item.full_context)

    def remove(self, item: Union[str, Dict[str, Any]]) -> None:
        if isinstance(item, str):
            if item in self.urls:
                self.urls.remove(item)
        elif isinstance(item, dict):
            for key in item:
                self.definitions.pop(key, None)

    @property
    def full_context(self) -> List[Union[str, Dict[str, Any]]]:
        result: List[Union[str, Dict[str, Any]]] = list(self.urls)
        if self.definitions:
            result.append(self.definitions)
        return result

    def __to_json__(self) -> Any:
        return self.full_context

    def __repr__(self) -> str:
        return f"LDContext({self.full_context})"

    def __len__(self) -> int:
        return len(self.full_context)

    def __getitem__(self, key: Any) -> Any:
        return self.full_context[key]

    def __add__(self: LDContextType, other: LDContext) -> LDContext:
        new_instance = self.__class__.from_any(self.full_context)
        if isinstance(other, LDContext):
            new_instance.add(other.full_context)
        return new_instance

    def __iadd__(self: LDContextType, other: LDContext) -> LDContextType:
        if isinstance(other, LDContext):
            self.add(other.full_context)
        return self
