from typing import Any, Dict, List, Optional, Union

import msgspec

from ..context import LDContext
from ..core.collection import Collection, OrderedCollection
from ..core.object import Object
from ..extra.cid import Multikey
from ..extra.security import CryptographicKey


class ActorEndpoints(Object):
    type: Optional[str] = msgspec.field(default="as:Endpoints")
    shared_inbox: Optional[Union[str, OrderedCollection]] = msgspec.field(default=None)

    @classmethod
    def model_validate(
        cls: type[ActorEndpoints], data: Any, context: Optional[Dict[str, Any]] = None
    ) -> ActorEndpoints:
        if not isinstance(data, dict):
            if isinstance(data, cls):
                return data
            raise ValueError(f"Expected dict, got {type(data)}")

        ld_context = context.get("ld_context") if context else None
        data_copy = data.copy()
        fields_to_validate = [
            "url",
            "attributedTo",
            "audience",
            "to",
            "bto",
            "cc",
            "bcc",
            "generator",
            "icon",
            "image",
            "inReplyTo",
            "location",
            "preview",
            "replies",
            "likes",
            "shares",
            "scope",
            "tag",
            "attachment",
            "sharedInbox",
        ]
        for field in fields_to_validate:
            if field in data_copy:
                data_copy[field] = cls._convert_field_to_model(
                    data_copy[field], ld_context
                )

        return super(Object, cls).model_validate(data_copy, context=context)


class Actor(Object):
    """
    Represents an ActivityStreams Actor.

    Actors are entities that can perform activities.
    """

    inbox: Optional[Union[str, OrderedCollection]] = msgspec.field(default=None)
    outbox: Optional[Union[str, OrderedCollection]] = msgspec.field(default=None)
    followers: Optional[Union[str, OrderedCollection, Collection]] = msgspec.field(
        default=None
    )
    following: Optional[Union[str, OrderedCollection, Collection]] = msgspec.field(
        default=None
    )
    liked: Optional[Union[str, OrderedCollection, Collection]] = msgspec.field(
        default=None
    )
    streams: Optional[Union[str, Collection]] = msgspec.field(default=None)
    preferred_username: Optional[str] = msgspec.field(default=None)
    endpoints: Optional[ActorEndpoints] = msgspec.field(default=None)
    discoverable: Optional[bool] = msgspec.field(default=None)
    indexable: Optional[bool] = msgspec.field(default=None)
    suspended: Optional[bool] = msgspec.field(default=None)
    memorial: Optional[bool] = msgspec.field(default=None)
    public_key: Optional[CryptographicKey] = msgspec.field(default=None)
    assertion_method: List[Multikey] = msgspec.field(default_factory=list)

    @classmethod
    def model_validate(
        cls: type[Actor], data: Any, context: Optional[Dict[str, Any]] = None
    ) -> Actor:
        if not isinstance(data, dict):
            if isinstance(data, cls):
                return data
            raise ValueError(f"Expected dict, got {type(data)}")

        ld_context = context.get("ld_context") if context else None
        data_copy = data.copy()
        fields_to_validate = [
            "url",
            "attributedTo",
            "audience",
            "to",
            "bto",
            "cc",
            "bcc",
            "generator",
            "icon",
            "image",
            "inReplyTo",
            "location",
            "preview",
            "replies",
            "likes",
            "shares",
            "scope",
            "tag",
            "attachment",
            "inbox",
            "outbox",
            "followers",
            "following",
            "liked",
            "streams",
            "endpoints",
            "publicKey",
            "assertionMethod",
        ]
        for field in fields_to_validate:
            if field in data_copy:
                data_copy[field] = cls._convert_field_to_model(
                    data_copy[field], ld_context
                )

        return super(Object, cls).model_validate(data_copy, context=context)

    @property
    def keys(self) -> List[Union[CryptographicKey, Multikey]]:
        """
        Provides a unified list of all keys associated with the actor.

        This property combines `public_key` and `assertion_method` into a single
        list for easier access.

        Returns:
            A list containing CryptographicKey and/or Multikey objects.
        """
        ret: List[Union[Multikey, CryptographicKey]] = []
        if self.public_key:
            ret.append(self.public_key)
        ret.extend(self.assertion_method)
        return ret

    def get_key(self, key_id: str) -> Optional[Union[CryptographicKey, Multikey]]:
        """
        Finds a key by its ID from all keys associated with the actor.

        Args:
            key_id: The ID of the key to find.

        Returns:
            The key object (CryptographicKey or Multikey) if found,
            otherwise None.
        """
        return next((key for key in self.keys if key.id == key_id), None)

    def _inference_context(self, result: dict) -> Dict[str, Any]:
        result = super()._inference_context(result)

        res_ctx = result.get("@context", [])
        dynamic_context = LDContext(res_ctx)
        dynamic_context.add("https://www.w3.org/ns/activitystreams")

        if result.get("publicKey"):
            dynamic_context.add("https://w3id.org/security/v1")
        if result.get("assertionMethod"):
            dynamic_context.add("https://w3id.org/did/v1")

        if result.get("manuallyApprovesFollowers"):
            dynamic_context.add(
                {"manuallyApprovesFollowers": "as:manuallyApprovesFollowers"}
            )

        tootcontext = {"toot": "http://joinmastodon.org/ns#"}

        if result.get("suspended"):
            dynamic_context.add({**tootcontext, "suspended": "toot:suspended"})
        if result.get("memorial"):
            dynamic_context.add({**tootcontext, "memorial": "toot:memorial"})

        if any(
            isinstance(item, (dict, msgspec.Struct))
            and getattr(item, "type", None) == "PropertyValue"
            for item in result.get("attachment", [])
        ):
            dynamic_context.add(
                {
                    "schema": "http://schema.org#",
                    "value": "schema:value",
                    "PropertyValue": "schema:PropertyValue",
                }
            )

        finalcontext = dynamic_context.full_context
        if finalcontext:
            result["@context"] = finalcontext

        return result


class Application(Actor):
    type: Optional[str] = msgspec.field(default="Application")


class Group(Actor):
    type: Optional[str] = msgspec.field(default="Group")


class Organization(Actor):
    type: Optional[str] = msgspec.field(default="Organization")


class Person(Actor):
    type: Optional[str] = msgspec.field(default="Person")


class Service(Actor):
    type: Optional[str] = msgspec.field(default="Service")
