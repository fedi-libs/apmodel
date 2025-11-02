from apmodel.core import Activity, Collection, Link, Object
from apmodel.loader import load
from apmodel.vocab import Note

# --- Test Data ---

OBJECT_NOTE_JSON = {
    "@context": "https://www.w3.org/ns/activitystreams",
    "id": "http://example.org/foo",
    "type": "Note",
    "name": "A Simple Note",
    "content": "This is a simple note",
}

OBJECT_WITH_EXTRA_PROP_JSON = {
    "@context": "https://www.w3.org/ns/activitystreams",
    "id": "http://example.org/foo-extra",
    "type": "Note",
    "name": "A Note with Extra",
    "content": "This note has a custom property.",
    "myCustomProperty": "Hello World",
}

LINK_JSON = {
    "@context": "https://www.w3.org/ns/activitystreams",
    "type": "Link",
    "href": "http://example.org/abc",
    "hreflang": "en",
    "mediaType": "text/html",
    "name": "An example link",
}

ACTIVITY_ADD_JSON = {
    "@context": "http://www.w3.org/ns/activitystreams",
    "type": "Add",
    "actor": {"type": "Person", "name": "Krista"},
    "object": {"type": "Image", "name": "Picture of my Cat"},
    "target": {"type": "Collection", "name": "My Cat Pics"},
}

COLLECTION_JSON = {
    "@context": "https://www.w3.org/ns/activitystreams",
    "summary": "Object history",
    "type": "Collection",
    "totalItems": 2,
    "items": [
        {"type": "Create", "actor": "http://www.test.example/sally"},
        {"type": "Like", "actor": "http://www.test.example/joe"},
    ],
}

# --- Tests ---


def test_load_object():
    """Tests loading a basic Object (Note)."""
    obj = load(OBJECT_NOTE_JSON)

    assert isinstance(obj, Note)
    assert isinstance(
        obj, Object
    )  # Verify it's also an instance of the base class
    assert obj.id == "http://example.org/foo"
    assert obj.type == "Note"
    assert obj.name == "A Simple Note"
    assert obj.content == "This is a simple note"
    assert not obj._extra  # _extra should be empty


def test_load_object_with_extra_properties():
    """Tests that unknown properties are loaded into the _extra dictionary."""
    obj = load(OBJECT_WITH_EXTRA_PROP_JSON)

    assert isinstance(obj, Note)
    assert obj.id == "http://example.org/foo-extra"
    assert "myCustomProperty" in obj._extra
    assert obj._extra["myCustomProperty"] == "Hello World"


def test_load_link():
    """Tests loading a Link object."""
    link = load(LINK_JSON)

    assert isinstance(link, Link)
    assert link.type == "Link"
    assert link.href == "http://example.org/abc"
    assert link.mediaType == "text/html"
    assert link.name == "An example link"


def test_load_activity():
    """Tests loading a basic Activity (Add)."""
    # The loader should recursively load nested objects
    activity = load(ACTIVITY_ADD_JSON)

    assert isinstance(activity, Activity)
    assert activity.type == "Add"

    # Test nested actor object
    assert isinstance(activity.actor, Object)
    assert activity.actor.type == "Person"
    assert activity.actor.name == "Krista"

    # Test nested object
    assert isinstance(activity.object, Object)
    assert activity.object.type == "Image"
    assert activity.object.name == "Picture of my Cat"

    # Test nested target
    assert isinstance(activity.target, Collection)
    assert activity.target.name == "My Cat Pics"


def test_load_collection():
    """Tests loading a Collection object."""
    collection = load(COLLECTION_JSON)

    assert isinstance(collection, Collection)
    assert collection.type == "Collection"
    assert collection.summary == "Object history"
    assert collection.totalItems == 2
    assert isinstance(collection.items, list)
    assert len(collection.items) == 2

    # Check that items in the collection are also loaded as model objects
    assert isinstance(collection.items[0], Activity)
    assert collection.items[0].type == "Create"
    assert collection.items[0].actor == "http://www.test.example/sally"

    assert isinstance(collection.items[1], Activity)
    assert collection.items[1].type == "Like"
    assert collection.items[1].actor == "http://www.test.example/joe"
