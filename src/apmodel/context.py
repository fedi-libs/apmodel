from __future__ import annotations

from typing import Any, Dict, List, TypeVar, Union, overload
from urllib.parse import urlparse, urlunparse

from pydantic_core import core_schema

LDContextType = TypeVar("LDContextType", bound="LDContext")


class LDContext:
    """
    Parses and manages a JSON-LD @context, ensuring uniqueness.

    - String URLs are stored in a list, with duplicates ignored.
    - Dictionary definitions are merged, with later values overwriting earlier
      ones for the same key.
    This provides a list-like interface to the full context.
    """

    def __init__(self, context: Any = None):
        self.urls: List[str] = []
        self.definitions: Dict[str, Any] = {}
        if context:
            self.add(context)

    def _parse_and_add(self, context: Any):
        """Parses and adds a context item, handling deduplication."""
        if not isinstance(context, list):
            context = [context]

        for item in context:
            if isinstance(item, str):
                # Add URL if not already present, preserving order
                if item not in self.urls:
                    self.urls.append(item)
            elif isinstance(item, dict):
                # Merge dictionary, overwriting existing keys
                self.definitions.update(item)

    def add(self, context: Any):
        """Adds a new item or list of items to the context."""
        self._parse_and_add(context)

    def remove(self, item: Union[str, dict]):
        """
        Removes an item from the context.
        - If item is a string, it's removed from the URL list.
        - If item is a dict, its keys are removed from the definitions.
        """
        if isinstance(item, str):
            if item in self.urls:
                self.urls.remove(item)
        elif isinstance(item, dict):
            for key in item:
                if key in self.definitions:
                    del self.definitions[key]

    @property
    def json(self) -> Dict[str, Any]:
        """
        Returns the merged dictionary of all JSON objects from the @context.
        """
        return self.definitions

    @property
    def full_context(self) -> List[Union[str, Dict[str, Any]]]:
        """
        Returns the full context as a list, with definitions merged into a single object.
        """
        result: List[Union[str, Dict[str, Any]]] = list(self.urls)
        if self.definitions:
            result.append(self.definitions)
        return result

    def __repr__(self) -> str:
        return f"LDContext({self.full_context})"

    def __len__(self) -> int:
        return len(self.full_context)

    def __iter__(self):
        return iter(self.full_context)

    @overload
    def __getitem__(self, key: int) -> Union[str, Dict[str, Any]]: ...

    @overload
    def __getitem__(self, key: slice) -> List[Union[str, Dict[str, Any]]]: ...

    def __getitem__(
        self, key: Union[int, slice]
    ) -> Union[Union[str, Dict[str, Any]], List[Union[str, Dict[str, Any]]]]:
        return self.full_context[key]

    def __add__(self: LDContextType, other: LDContext) -> LDContextType:
        """Merges two LDContext instances into a new one."""
        new_context = self.__class__(self.full_context)
        new_context.add(other.full_context)
        return new_context

    def __iadd__(self: LDContextType, other: LDContext) -> LDContextType:
        """Merges another LDContext instance into this one."""
        self.add(other.full_context)
        return self

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,
        handler: Any,
    ) -> core_schema.CoreSchema:
        """
        Defines how Pydantic should handle the LDContext type.
        """
        from_any_schema = core_schema.no_info_plain_validator_function(cls)

        to_full_context_serializer = (
            core_schema.plain_serializer_function_ser_schema(
                lambda instance: instance.full_context
            )
        )

        return core_schema.json_or_python_schema(
            json_schema=from_any_schema,
            python_schema=from_any_schema,
            serialization=to_full_context_serializer,
        )


def _get_namespace_base(uri: str) -> Union[str, None]:
    parsed_uri = urlparse(uri)

    if parsed_uri.fragment:
        base_url = urlunparse(parsed_uri._replace(fragment=""))

        if not base_url.endswith("#") and not base_url.endswith("/"):
            return base_url + "#"

        return base_url

    elif parsed_uri.path and parsed_uri.path != "/":
        path_segments = parsed_uri.path.rstrip("/").split("/")
        local_name = path_segments[-1]

        if len(path_segments) > 1:
            namespace_base_path = parsed_uri.path[: -len(local_name)]
            base_url = urlunparse(
                parsed_uri._replace(
                    path=namespace_base_path, params="", query="", fragment=""
                )
            )

            if base_url and not (
                base_url.endswith("/") or base_url.endswith("#")
            ):
                return base_url + "/"

            return base_url

    return None

def generate_context_from_expanded(expanded_json_ld: List[Dict[str, Any]], orig_context: LDContext = LDContext()) -> Dict[str, List[Union[str, Dict[str, Any]]]]:
    uris_to_process = set()

    for item in expanded_json_ld:
        entity_id = item.get("@id")
        for key in item.keys():
                if key in ("@id", "@type", "@context"):
                            continue
                uris_to_process.add(key)
                
                if isinstance(item[key], list):
                    for sub_item in item[key]:
                        if isinstance(sub_item, dict) and "@id" in sub_item and "://" in sub_item["@id"]:
                            sub_id = sub_item["@id"]

        if "@type" in item:
            for type_uri in item["@type"]:
                if "://" in type_uri:
                    uris_to_process.add(type_uri)

    context_obj = LDContext()
    
    for uri in uris_to_process:
        base_url = _get_namespace_base(uri)
        
        if base_url:
            context_obj.add(base_url)

    context_obj = context_obj + orig_context
    return {"@context": context_obj.full_context}