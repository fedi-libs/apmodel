from cryptography.hazmat.primitives.asymmetric import ed25519, rsa

from apmodel.extra.cid import Multikey


def test_multikey_creation():
    # Test creating a Multikey instance
    multikey = Multikey(
        id="did:example:123#key-1",
        controller="did:example:123",
        public_key_multibase="z6Mkj4b13pyZeBuFq47Dyh5D84iJ6h779m6w585q3cN6k4o3",
    )

    assert multikey.id == "did:example:123#key-1"
    assert multikey.controller == "did:example:123"
    assert (
        multikey.public_key_multibase
        == "z6Mkj4b13pyZeBuFq47Dyh5D84iJ6h779m6w585q3cN6k4o3"
    )
    assert multikey.type == "Multikey"


def test_multikey_public_key_property():
    # Generate an Ed25519 key pair for testing
    private_key = ed25519.Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    # Encode the public key in multibase format (this would normally be done through the setter)
    from apmodel._core.key import _encode_public_key_as_multibase

    multibase_encoded = _encode_public_key_as_multibase(public_key)

    # Create a Multikey instance
    multikey = Multikey(
        id="did:example:123#key-1",
        controller="did:example:123",
        public_key_multibase=multibase_encoded,
    )

    # Access the public key property
    retrieved_public_key = multikey.public_key

    assert retrieved_public_key is not None
    assert isinstance(retrieved_public_key, ed25519.Ed25519PublicKey)


def test_multikey_private_key_property():
    # Generate an Ed25519 key pair for testing
    private_key = ed25519.Ed25519PrivateKey.generate()

    # Encode the private key in multibase format (this would normally be done through the setter)
    from apmodel._core.key import _encode_private_key_as_multibase

    multibase_encoded = _encode_private_key_as_multibase(private_key)

    # Create a Multikey instance
    multikey = Multikey(
        id="did:example:123#key-1",
        controller="did:example:123",
        secret_key_multibase=multibase_encoded,
    )

    # Access the private key property
    retrieved_private_key = multikey.private_key

    assert retrieved_private_key is not None
    assert isinstance(retrieved_private_key, ed25519.Ed25519PrivateKey)


def test_multikey_set_public_key_with_ed25519():
    # Generate an Ed25519 key pair for testing
    private_key = ed25519.Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    # Create a Multikey instance
    multikey = Multikey(id="did:example:123#key-1", controller="did:example:123")

    # Set the public key
    multikey.public_key = public_key

    # Check that the multibase representation was set
    assert multikey.public_key_multibase is not None

    # Check that the public key property returns the correct key
    retrieved_key = multikey.public_key
    assert retrieved_key is not None
    assert isinstance(retrieved_key, ed25519.Ed25519PublicKey)


def test_multikey_set_public_key_with_rsa():
    # Generate an RSA key pair for testing
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()

    # Create a Multikey instance
    multikey = Multikey(id="did:example:123#key-1", controller="did:example:123")

    # Set the public key
    multikey.public_key = public_key

    # Check that the multibase representation was set
    assert multikey.public_key_multibase is not None

    # Check that the public key property returns the correct key
    retrieved_key = multikey.public_key
    assert retrieved_key is not None
    assert isinstance(retrieved_key, rsa.RSAPublicKey)


def test_multikey_set_public_key_with_private_key():
    # Generate an Ed25519 key pair for testing
    private_key = ed25519.Ed25519PrivateKey.generate()

    # Create a Multikey instance
    multikey = Multikey(id="did:example:123#key-1", controller="did:example:123")

    # Set the public key using the private key (should extract the public key)
    multikey.public_key = private_key

    # Check that the multibase representation was set
    assert multikey.public_key_multibase is not None

    # Check that the public key property returns the correct key
    retrieved_key = multikey.public_key
    assert retrieved_key is not None
    assert isinstance(retrieved_key, ed25519.Ed25519PublicKey)


def test_multikey_set_private_key():
    # Generate an Ed25519 key pair for testing
    private_key = ed25519.Ed25519PrivateKey.generate()

    # Create a Multikey instance
    multikey = Multikey(id="did:example:123#key-1", controller="did:example:123")

    # Set the private key
    multikey.private_key = private_key

    # Check that the multibase representation was set
    assert multikey.secret_key_multibase is not None

    # Check that the private key property returns the correct key
    retrieved_key = multikey.private_key
    assert retrieved_key is not None
    assert isinstance(retrieved_key, ed25519.Ed25519PrivateKey)


def test_multikey_serialization():
    # Create a Multikey instance
    multikey = Multikey(
        id="did:example:123#key-1",
        controller="did:example:123",
        public_key_multibase="z6Mkj4b13pyZeBuFq47Dyh5D84iJ6h779m6w585q3cN6k4o3",
    )

    # Check serialization
    serialized = multikey.model_dump(by_alias=True)
    assert serialized["id"] == "did:example:123#key-1"
    assert serialized["controller"] == "did:example:123"
    assert (
        serialized["publicKeyMultibase"]
        == "z6Mkj4b13pyZeBuFq47Dyh5D84iJ6h779m6w585q3cN6k4o3"
    )
    assert serialized["type"] == "Multikey"
