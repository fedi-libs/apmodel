import apmodel
import pytest
from datetime import datetime

from apmodel.vocab.tombstone import Tombstone
from apmodel.core.object import Object


def test_tombstone_creation():
    # Test creating a Tombstone instance
    tombstone = Tombstone(id="http://example.com/object/1", name="Deleted Object")

    assert tombstone.id == "http://example.com/object/1"
    assert tombstone.name == "Deleted Object"
    assert tombstone.type == "Tombstone"


def test_tombstone_with_former_type():
    # Test creating a Tombstone with former_type field
    tombstone = Tombstone(
        id="http://example.com/object/1", name="Deleted Object", former_type="Note"
    )

    assert tombstone.id == "http://example.com/object/1"
    assert tombstone.name == "Deleted Object"
    assert tombstone.former_type == "Note"


def test_tombstone_with_deleted_datetime():
    # Test creating a Tombstone with deleted field as datetime
    dt = datetime(2023, 1, 1, 12, 0, 0)
    tombstone = Tombstone(
        id="http://example.com/object/1", name="Deleted Object", deleted=dt
    )

    assert tombstone.id == "http://example.com/object/1"
    assert tombstone.name == "Deleted Object"
    assert tombstone.deleted == dt


def test_tombstone_with_deleted_string():
    # Test creating a Tombstone with deleted field as string
    tombstone = Tombstone(
        id="http://example.com/object/1",
        name="Deleted Object",
        deleted="2023-01-01T12:00:00Z",
    )

    assert tombstone.id == "http://example.com/object/1"
    assert tombstone.name == "Deleted Object"
    # The string should be parsed to datetime
    assert isinstance(tombstone.deleted, datetime)


def test_tombstone_invalid_deleted_format():
    # Test creating a Tombstone with invalid deleted format
    with pytest.raises(ValueError):
        Tombstone(
            id="http://example.com/object/1",
            name="Deleted Object",
            deleted="invalid-date-format",
        )


def test_tombstone_serialization_with_datetime():
    # Test serialization of a Tombstone with datetime deleted field
    dt = datetime(2023, 1, 1, 12, 0, 0)
    tombstone = Tombstone(
        id="http://example.com/object/1", name="Deleted Object", deleted=dt
    )

    serialized = tombstone.model_dump(by_alias=True)

    assert "id" in serialized
    assert "name" in serialized
    assert "deleted" in serialized
    # The datetime should be serialized as an ISO string, but the Z suffix behavior might differ
    # Check that it starts with the expected date/time part
    assert serialized["deleted"].startswith("2023-01-01T12:00:00")


def test_tombstone_serialization_with_string():
    # Test serialization of a Tombstone with string deleted field
    tombstone = Tombstone(
        id="http://example.com/object/1",
        name="Deleted Object",
        deleted="2023-01-01T12:00:00Z",
    )

    serialized = tombstone.model_dump(by_alias=True)

    assert "id" in serialized
    assert "name" in serialized
    assert "deleted" in serialized
    # The datetime should be serialized as an ISO string with Z suffix
    assert serialized["deleted"] == "2023-01-01T12:00:00Z"


def test_tombstone_with_object_former_type():
    # Test creating a Tombstone with Object in former_type field
    nested_obj = Object(id="http://example.com/former_type", name="Former Type")
    tombstone = Tombstone(
        id="http://example.com/object/1", name="Deleted Object", former_type=nested_obj
    )

    assert tombstone.id == "http://example.com/object/1"
    assert tombstone.name == "Deleted Object"
    # The nested object should be loaded properly
    assert tombstone.former_type is not None
    assert hasattr(tombstone.former_type, "id")


def test_tombstone_serialization():
    # Test full serialization of a Tombstone
    tombstone = Tombstone(
        id="http://example.com/object/1",
        name="Deleted Object",
        former_type="Note",
        deleted="2023-01-01T12:00:00Z",
    )

    serialized = apmodel.to_dict(tombstone)

    assert serialized["id"] == "http://example.com/object/1"
    assert serialized["name"] == "Deleted Object"
    assert serialized["formerType"] == "Note"
    assert serialized["deleted"] == "2023-01-01T12:00:00Z"
    assert serialized["type"] == "Tombstone"
