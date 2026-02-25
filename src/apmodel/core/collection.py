from __future__ import annotations

from typing import Any, List, Optional, Union, Dict

import msgspec
from .link import Link
from .object import Object


class Collection(Object):
    type: Optional[str] = msgspec.field(default="Collection")

    total_items: Optional[int] = msgspec.field(default=None)
    current: Optional[Union[str, CollectionPage, OrderedCollectionPage, Link]] = msgspec.field(
        default=None
    )
    first: Optional[Union[str, CollectionPage, OrderedCollectionPage, Link]] = msgspec.field(
        default=None
    )
    last: Optional[Union[str, CollectionPage, OrderedCollectionPage, Link]] = msgspec.field(
        default=None
    )
    items: Optional[List[Union[Object, Link, Dict[str, Any]]]] = msgspec.field(default=None)

    @classmethod
    def model_validate(cls: type[Collection], data: Any, context: Optional[Dict[str, Any]] = None) -> Collection:
        if not isinstance(data, dict):
            if isinstance(data, cls):
                return data
            raise ValueError(f"Expected dict, got {type(data)}")

        ld_context = context.get("ld_context") if context else None
        
        data_copy = data.copy()
        # ActivityPubModel field conversion logic
        fields_to_validate = [
            "url", "attributedTo", "audience", "to", "bto", "cc", "bcc",
            "generator", "icon", "image", "inReplyTo", "location", "preview",
            "replies", "likes", "shares", "scope", "tag", "attachment",
            "current", "first", "last", "items"
        ]
        for field in fields_to_validate:
            if field in data_copy:
                data_copy[field] = cls._convert_field_to_model(data_copy[field], ld_context)
        
        return super(Object, cls).model_validate(data_copy, context=context)


class CollectionPage(Collection):
    type: Optional[str] = msgspec.field(default="CollectionPage")

    part_of: Optional[Union[str, Collection, Link]] = msgspec.field(default=None)

    next: Optional[Union[str, CollectionPage, Link]] = msgspec.field(default=None)
    prev: Optional[Union[str, CollectionPage, Link]] = msgspec.field(default=None)

    @classmethod
    def model_validate(cls: type[CollectionPage], data: Any, context: Optional[Dict[str, Any]] = None) -> CollectionPage:
        if not isinstance(data, dict):
            if isinstance(data, cls):
                return data
            raise ValueError(f"Expected dict, got {type(data)}")

        ld_context = context.get("ld_context") if context else None
        
        data_copy = data.copy()
        fields_to_validate = [
            "url", "attributedTo", "audience", "to", "bto", "cc", "bcc",
            "generator", "icon", "image", "inReplyTo", "location", "preview",
            "replies", "likes", "shares", "scope", "tag", "attachment",
            "current", "first", "last", "items", "partOf", "next", "prev"
        ]
        for field in fields_to_validate:
            if field in data_copy:
                data_copy[field] = cls._convert_field_to_model(data_copy[field], ld_context)
        
        return super(Object, cls).model_validate(data_copy, context=context)


class OrderedCollection(Collection):
    type: Optional[str] = msgspec.field(default="OrderedCollection")
    ordered_items: Optional[List[Union[Object, Link, Dict[str, Any], str]]] = msgspec.field(
        default=None
    )

    @classmethod
    def model_validate(cls: type[OrderedCollection], data: Any, context: Optional[Dict[str, Any]] = None) -> OrderedCollection:
        if not isinstance(data, dict):
            if isinstance(data, cls):
                return data
            raise ValueError(f"Expected dict, got {type(data)}")

        ld_context = context.get("ld_context") if context else None
        
        data_copy = data.copy()
        fields_to_validate = [
            "url", "attributedTo", "audience", "to", "bto", "cc", "bcc",
            "generator", "icon", "image", "inReplyTo", "location", "preview",
            "replies", "likes", "shares", "scope", "tag", "attachment",
            "current", "first", "last", "items", "orderedItems"
        ]
        for field in fields_to_validate:
            if field in data_copy:
                data_copy[field] = cls._convert_field_to_model(data_copy[field], ld_context)
        
        return super(Object, cls).model_validate(data_copy, context=context)


class OrderedCollectionPage(OrderedCollection, CollectionPage):
    type: Optional[str] = msgspec.field(default="OrderedCollectionPage")

    start_index: Optional[int] = msgspec.field(default=None)

    @classmethod
    def model_validate(cls: type[OrderedCollectionPage], data: Any, context: Optional[Dict[str, Any]] = None) -> OrderedCollectionPage:
        if not isinstance(data, dict):
            if isinstance(data, cls):
                return data
            raise ValueError(f"Expected dict, got {type(data)}")

        ld_context = context.get("ld_context") if context else None
        
        data_copy = data.copy()
        fields_to_validate = [
            "url", "attributedTo", "audience", "to", "bto", "cc", "bcc",
            "generator", "icon", "image", "inReplyTo", "location", "preview",
            "replies", "likes", "shares", "scope", "tag", "attachment",
            "current", "first", "last", "items", "partOf", "next", "prev", "orderedItems"
        ]
        for field in fields_to_validate:
            if field in data_copy:
                data_copy[field] = cls._convert_field_to_model(data_copy[field], ld_context)
        
        return super(Object, cls).model_validate(data_copy, context=context)
