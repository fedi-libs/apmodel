from typing import Any, Dict, List, Optional

from pydantic import Field

from ..context import LDContext
from ..core.collection import Collection, OrderedCollection
from ..core.object import Object
from ..extra.cid import Multikey
from ..extra.security import CryptographicKey


class ActorEndpoints(Object):
    type: str = Field(default="as:Endpoints", kw_only=True, frozen=True)
    shared_inbox: Optional[str | OrderedCollection] = Field(default=None)


class Actor(Object):
    """
    Represents an ActivityStreams Actor.

    Actors are entities that can perform activities.
    """

    inbox: Optional[str | OrderedCollection] = Field(default=None)
    outbox: Optional[str | OrderedCollection] = Field(default=None)
    followers: Optional[str | OrderedCollection | Collection] = Field(default=None)
    following: Optional[str | OrderedCollection | Collection] = Field(default=None)
    liked: Optional[str | OrderedCollection | Collection] = Field(default=None)
    streams: Optional[str | Collection] = Field(default=None)
    preferred_username: Optional[str] = Field(default=None)
    endpoints: Optional[ActorEndpoints] = Field(default=None)
    discoverable: Optional[bool] = Field(default=None)
    indexable: Optional[bool] = Field(default=None)
    suspended: Optional[bool] = Field(default=None)
    memorial: Optional[bool] = Field(default=None)
    public_key: Optional[CryptographicKey] = Field(default=None)
    assertion_method: List[Multikey] = Field(default_factory=list)

    @property
    def keys(self) -> List[CryptographicKey | Multikey]:
        """
        Provides a unified list of all keys associated with the actor.

        This property combines `public_key` and `assertion_method` into a single
        list for easier access.

        Returns:
            A list containing CryptographicKey and/or Multikey objects.
        """
        ret: List[Multikey | CryptographicKey] = []
        if self.public_key:
            ret.append(self.public_key)
        ret.extend(self.assertion_method)
        return ret

    def get_key(self, key_id: str) -> Optional[CryptographicKey | Multikey]:
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
            isinstance(item, dict) and item.get("type") == "PropertyValue"
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
    type: str = Field(default="Application", kw_only=True, frozen=True)


class Group(Actor):
    type: str = Field(default="Group", kw_only=True, frozen=True)


class Organization(Actor):
    type: str = Field(default="Organization", kw_only=True, frozen=True)


class Person(Actor):
    type: str = Field(default="Person", kw_only=True, frozen=True)


class Service(Actor):
    type: str = Field(default="Service", kw_only=True, frozen=True)
