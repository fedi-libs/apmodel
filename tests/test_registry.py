import sys
from typing import Dict, Optional, Type, Union

import pytest
from pydantic import Field

from apmodel.core.object import Object
from apmodel.registry import ModelRegistry, _load_model_cls
from apmodel.types import ActivityPubModel

MINIMAL_PRELOADS: Dict[str, Union[str, Type[ActivityPubModel]]] = {
    "https://www.w3.org/ns/activitystreams#Object": "apmodel.core.object.Object",
    "https://www.w3.org/ns/activitystreams#Person": "apmodel.vocab.actor.Person",
}


@pytest.fixture
def test_registry() -> ModelRegistry:
    """Provides a clean ModelRegistry instance with minimal preloads for each test."""
    return ModelRegistry(preload_mapping=MINIMAL_PRELOADS.copy())


def test_get_model(test_registry: ModelRegistry):
    """Tests basic model retrieval."""
    model_class = test_registry.get("https://www.w3.org/ns/activitystreams#Object")
    assert model_class is Object


def test_lazy_loading(test_registry: ModelRegistry):
    """Ensures that models are loaded only when requested."""
    module_path = "apmodel.vocab.actor"

    original_module = sys.modules.pop(module_path, None)

    try:
        assert module_path not in sys.modules

        person_class = test_registry.get("https://www.w3.org/ns/activitystreams#Person")

        assert module_path in sys.modules
        from apmodel.vocab.actor import Person

        assert person_class is Person
    finally:
        if original_module:
            sys.modules[module_path] = original_module


def test_get_non_existent_model(test_registry: ModelRegistry):
    """Tests that getting a non-existent model returns None."""
    assert test_registry.get("https://example.com/ns#NonExistent") is None


def test_register_custom_model(test_registry: ModelRegistry):
    """Tests registration of a new custom model."""

    class CustomObject(Object):
        type: str = Field("https://example.com/ns#CustomObject", frozen=True)

    test_registry.register(CustomObject, "https://example.com/ns#CustomObject")
    retrieved_class = test_registry.get("https://example.com/ns#CustomObject")
    assert retrieved_class is CustomObject


def test_overwrite_existing_model(test_registry: ModelRegistry):
    """Tests that a registered model can be overwritten by a subclass."""
    from apmodel.vocab.actor import Person

    class ExtendedPerson(Person):
        pass

    test_registry.register(
        ExtendedPerson, "https://www.w3.org/ns/activitystreams#Person"
    )
    retrieved_class = test_registry.get("https://www.w3.org/ns/activitystreams#Person")
    assert retrieved_class is ExtendedPerson


def test_overwrite_with_invalid_inheritance(test_registry: ModelRegistry):
    """Tests that overwriting with a non-subclass issues a warning."""
    from apmodel.vocab.actor import Person

    class UnrelatedClass(ActivityPubModel):
        pass

    with pytest.warns(UserWarning, match="conflicts with existing model"):
        test_registry.register(
            UnrelatedClass, "https://www.w3.org/ns/activitystreams#Person"
        )

    retrieved_class = test_registry.get("https://www.w3.org/ns/activitystreams#Person")
    assert retrieved_class is Person


def test_load_model_cls():
    """Tests the private _load_model_cls function."""
    cls = _load_model_cls("apmodel.core.object.Object")
    assert cls is Object


def test_has_method(test_registry: ModelRegistry):
    """Tests the `has` method for registered and unregistered models."""
    assert test_registry.has("https://www.w3.org/ns/activitystreams#Object") is True
    assert test_registry.has("https://example.com/ns#NonExistent") is False
