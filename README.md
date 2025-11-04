# apmodel

[![PyPI version](https://badge.fury.io/py/apmodel.svg)](https://badge.fury.io/py/apmodel)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

Pydantic models for ActivityStreams 2.0, NodeInfo, and other Fediverse-related vocabularies.

`apmodel` provides model implementations for:
- Activity Streams 2.0
- [NodeInfo](https://nodeinfo.diasporafoundation.org/protocol.html) (2.0 and 2.1)
- [CryptographicKey](https://w3c-ccg.github.io/security-vocab/contexts/security-v1.jsonld) (Security Vocabulary v1)
- [Multikey](https://w3c-ccg.github.io/multikey/) and [DataIntegrityProof](https://w3c-ccg.github.io/data-integrity-spec/) (Controlled Identifiers v1.0)
- [PropertyValue](https://schema.org/PropertyValue) (schema.org)

## Features

- **Type-Safe Models**: Leverages Pydantic for robust and type-safe data validation and manipulation.
- **Automatic Model Loading**: A `load` function that automatically reads the `type` field from a dictionary and converts it to the correct Pydantic model.
- **JSON-LD Aware**: Designed to work seamlessly with JSON-LD data, automatically handling expanded formats (e.g., values wrapped in arrays).
- **Flexible Deserialization**: Handles unknown properties gracefully, allowing you to work with custom extensions in the ActivityPub ecosystem. Extra fields are attached directly to the model object.
- **Comprehensive Vocabulary**: Includes a wide range of models from the ActivityStreams vocabulary, as well as common extensions used in the Fediverse.

## Installation

```bash
pip install apmodel
```

## Usage

### Loading Objects

Use the `apmodel.load()` function to parse a dictionary into a specific ActivityStreams model. The function inspects the `type` field to determine the correct model.

```python
import apmodel

# Example ActivityStreams Note object as a dictionary
note_data = {
    "@context": "https://www.w3.org/ns/activitystreams",
    "type": "Note",
    "content": "This is a simple note.",
    "published": "2025-05-10T12:00:00Z",
    "to": ["https://www.w3.org/ns/activitystreams#Public"],
    "cc": ["https://example.com/users/alice/followers"]
}

# Load the dictionary into a Note object
note_object = apmodel.load(note_data)

# note_object is now an instance of apmodel.vocab.Note
print(type(note_object))
# > <class 'apmodel.vocab.note.Note'>

# You can access attributes with type safety
print(note_object.content)
# > This is a simple note.

# The context is also parsed into an LDContext object
print(note_object.context.to_json())
# > ["https://www.w3.org/ns/activitystreams"]
```

### Creating Objects

You can also create objects programmatically.

```python
from apmodel.vocab import Create
from apmodel.vocab import Note

note = Note(content="My new note!")
create_activity = Create(
    actor="https://example.com/users/bob",
    object=note,
)

# The model can be converted back to a dictionary
# (Note: a dedicated `dump` function is not yet implemented,
# but you can use Pydantic's `model_dump` for now)
activity_dict = create_activity.model_dump(by_alias=True, exclude_none=True)

import json
print(json.dumps(activity_dict, indent=2))
```

This will output:
```json
{
  "@context": [
    "https://www.w3.org/ns/activitystreams"
  ],
  "@type": "Create",
  "actor": "https://example.com/users/bob",
  "object": {
    "@context": [
      "https://www.w3.org/ns/activitystreams"
    ],
    "@type": "Note",
    "content": "My new note!"
  }
}
```

## Development

This project uses [Task](https://taskfile.dev/) for running scripts.

### Setup Dev Environment

Installs development dependencies.

```bash
task
```

### Run Tests

```bash
task test
```

## License

This project is licensed under the MIT License.