# apmodel

[![PyPI - Version](https://img.shields.io/pypi/v/apmodel)](https://pypi.org/project/apmodel)
[![Tests](https://github.com/fedi-libs/apmodel/actions/workflows/test.yml/badge.svg)](https://github.com/fedi-libs/apmodel/actions/workflows/test.yml)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/fedi-libs/apmodel/develop.svg)](https://results.pre-commit.ci/latest/github/fedi-libs/apmodel/develop)

apmodel is a Python library that provides model implementations for various decentralized social web protocols.

It is designed to easily parse and handle JSON data from sources like Mastodon, Misskey, and other Fediverse software.

this branch is experiment of migrate apmodel to msgspec from pydantic v2. you can use this branch as drop-in alternative but maybe have some imcompatibilities.

If using uv, you can override apmodel as this code:

```toml
[tool.uv.overrides]
"apmodel" = { git = "https://github.com/fedi-libs/apmodel.git", rev = "dev/msgspec" }
```

## Features

- **Automatic Model Resolution**: The `apmodel.load` function automatically deserializes a JSON object into the appropriate Python object by reading its `type` field. If no matching model is found, the original dictionary is returned.
- **Flexible Deserialization**: Any properties in the JSON that do not have a corresponding field in the model are collected into an `model_extra` dictionary. This ensures no data is lost.
- **Type Hinting**: Fully type-hinted for a better development experience and robust static analysis.

## Installation

```bash
pip install apmodel

# uv
uv add apmodel
```

## Usage

Here is a basic example of how to parse an ActivityStreams 2.0 `Note` object from a JSON string.

```python
import apmodel

# Example JSON from a Fediverse server
json_data = {
  "@context": "https://www.w3.org/ns/activitystreams",
  "id": "https://example.com/users/alice/statuses/1",
  "type": "Note",
  "published": "2023-12-25T12:00:00Z",
  "attributedTo": "https://example.com/users/alice",
  "content": "<p>Hello, world!</p>",
  "to": ["https://www.w3.org/ns/activitystreams#Public"],
  "cc": ["https://example.com/users/alice/followers"]
}

# Load the JSON into an apmodel object
obj = apmodel.load(json_data)

# Now you can access properties with type safety
if isinstance(obj, apmodel.vocab.Note):
    print(f"Type: {obj.type}")
    print(f"Content: {obj.content}")
    print(f"Published: {obj.published}")

# >> Type: Note
# >> Content: <p>Hello, world!</p>
# >> Published: 2023-12-25 12:00:00+00:00
```

## Documentation

https://fedi-libs.github.io/apmodel

## Supported Specifications

`apmodel` provides models for the following specifications:

- **Activity Streams 2.0**: Core types like `Object`, `Activity`, `Collection`, and `Link`.
- **Activity Vocabulary**: All types.
- **Security Vocabulary v1**: `CryptographicKey` (`Key`).
- **Controlled Identifiers v1.0**: `Multikey` and `DataIntegrityProof`.
- **schema.org**: `PropertyValue`.
- **NodeInfo 2.0/2.1**
- **Litepub**: `EmojiReact`
- **Others**: `Emoji` and `Hashtag`

## Development

This project uses [Task](https://taskfile.dev/) for running scripts. You need to install it first.

- **Setup dev environment**:

    ```bash
    task
    ```

- **Run tests with Pytest**:

    ```bash
    task test
    ```

- **Build packages for PyPI**:

    ```bash
    task build
    ```

- **Development Document**:
    ```bash
    task docs:dev
    ```

## License

MIT License
