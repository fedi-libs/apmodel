# Registry

The `apmodel.registry` module manages the mapping between Activity Streams types (URIs) and their corresponding Python model classes. This allows `apmodel.load()` to automatically convert JSON-LD data into the correct Pydantic model instances.

## How the Registry Works

At its core, the `registry` holds a dictionary where keys are Activity Streams type URIs (e.g., "https://www.w3.org/ns/activitystreams#Person") and values are either:

1. The actual Python class corresponding to that type.

2. A string representing the import path to that class (e.g., "apmodel.vocab.actor.Person").

This design supports **lazy loading**, improving application startup performance by only importing model classes when they are actually needed.

## Accessing Models from the Registry

You can retrieve a registered model class using the `registry.get()` method.

```python
from apmodel.registry import registry

# Retrieve a standard Activity Streams model
Person = registry.get("https://www.w3.org/ns/activitystreams#Person")
print(Person)
# Output: <class 'apmodel.vocab.actor.Person'> (or similar)

# If the model was not yet loaded, it will be imported dynamically
# and then returned. Subsequent calls will use the cached class.
```

## Registering Custom Models

You can register your own custom Pydantic models with the registry. Your custom model should typically inherit from `apmodel.types.ActivityPubModel` (or a more specific `apmodel` base class like `apmodel.core.Object`) to ensure compatibility.

```python
from pydantic import Field
from apmodel.registry import registry
from apmodel.core import Object # Or a more specific base class

class MyCustomObject(Object[str | None]):
    type: str = Field("https://example.com/ns#MyCustomObject", frozen=True)
    my_property: str

# Register your custom model
registry.register(MyCustomObject, "https://example.com/ns#MyCustomObject")

# Now apmodel.load() can recognize and use your custom model
data = {
    "@context": "https://www.w3.org/ns/activitystreams",
    "type": "https://example.com/ns#MyCustomObject",
    "myProperty": "Hello Custom Model!"
}
instance = apmodel.load(data)
print(instance)
# Output: MyCustomObject(type='https://example.com/ns#MyCustomObject', my_property='Hello Custom Model!', extra={})
```

## Overwriting Existing Models

The `registry.register()` method can also be used to overwrite existing registered models. This is particularly useful if you want to extend or modify the behavior of a standard Activity Streams model.

When overwriting, the registry checks for inheritance relationships. If the new class (`model_cls`) is a subclass of the already registered class for `model_type`, and the existing class is not one of the base ActivityPub models (like `Object`, `Activity`), then the new class will replace the old one. Otherwise, a warning will be issued, and the registration might be skipped to prevent unintended overrides of core functionality.

```python
from pydantic import Field
from apmodel.registry import registry
from apmodel.vocab.actor import Person

# Define an extended Person model
class MyExtendedPerson(Person):
    my_custom_field: str = Field(default="default value")

# Overwrite the standard Person model
# This will succeed because MyExtendedPerson is a subclass of Person
registry.register(MyExtendedPerson, "https://www.w3.org/ns/activitystreams#Person")

# Now, loading a Person will use MyExtendedPerson
data = {
    "@context": "https://www.w3.org/ns/activitystreams",
    "type": "Person",
    "name": "Alice"
}
instance = apmodel.load(data)
print(instance)
# Output: MyExtendedPerson(type='Person', name='Alice', my_custom_field='default value', ...)
```

## Lazy Loading for Performance

To optimize startup performance, the `apmodel.registry` implements **lazy loading**.
Initially, the `TYPE_MAPPING` (defined in `_core._initial._registry_bootstrap.py`) stores model classes not as direct class objects, but as string representations of their import paths.

When `registry.get()` is called for a specific `model_type`, the registry checks if the corresponding class has already been loaded. If not, it uses `importlib` to dynamically import the module and retrieve the class object, then caches this class for future use.

This means that `apmodel` only loads the model definitions that are actively requested by your application, significantly reducing the initial memory footprint and speeding up the `import apmodel` process compared to eagerly loading all available models.

## Other Registry Methods

*   `registry.all() -> Dict[str, Type[ActivityPubModel]]`: Returns a dictionary of all registered models. **Note:** Calling this method will trigger the dynamic loading of all models that have not yet been loaded, potentially impacting performance if called unnecessarily at startup.
*   `registry.has(model_type: str) -> bool`: Checks if a model type is registered in the registry.
