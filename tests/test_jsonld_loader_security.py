
import socket
from unittest.mock import MagicMock, patch

import pytest
from pyld import jsonld

from apmodel._jsonld import create_document_loader


def test_load_context_from_loopback_address_raises_error():
    """
    Tests that attempting to load a JSON-LD context from a loopback address
    (127.0.0.1) raises a JsonLdError to prevent SSRF vulnerabilities.
    """
    loader = create_document_loader()
    url = "http://localhost/context.jsonld"

    with patch("socket.gethostbyname", return_value="127.0.0.1"):
        with pytest.raises(jsonld.JsonLdError) as excinfo:
            loader(url)
        assert "Loading from local or private network is not allowed." in str(
            excinfo.value
        )


def test_load_context_from_private_network_address_raises_error():
    """
    Tests that attempting to load a JSON-LD context from a private network
    address (192.168.1.1) raises a JsonLdError.
    """
    loader = create_document_loader()
    url = "http://example.internal/context.jsonld"

    with patch("socket.gethostbyname", return_value="192.168.1.1"):
        with pytest.raises(jsonld.JsonLdError) as excinfo:
            loader(url)
        assert "Loading from local or private network is not allowed." in str(
            excinfo.value
        )


def test_load_context_from_unresolvable_hostname_raises_error():
    """
    Tests that attempting to load a JSON-LD context from a hostname that
    cannot be resolved raises a JsonLdError.
    """
    loader = create_document_loader()
    url = "http://this-is-not-a-real-hostname/context.jsonld"

    with patch(
        "socket.gethostbyname", side_effect=socket.gaierror("not found")
    ):
        with pytest.raises(jsonld.JsonLdError) as excinfo:
            loader(url)
        assert "Could not resolve hostname." in str(excinfo.value)


@patch("pyld.documentloader.requests.requests_document_loader")
def test_load_context_from_public_address_succeeds(mock_requests_loader_factory):
    """
    Tests that loading a JSON-LD context from a public address is allowed
    and proceeds as expected.
    """
    loader = create_document_loader()
    url = "http://schema.org/context.jsonld"
    expected_doc = {"@context": "http://schema.org"}

    # Mock the inner loader function that the factory returns
    mock_inner_loader = MagicMock()
    mock_inner_loader.return_value = {
        "contextUrl": None,
        "documentUrl": url,
        "document": expected_doc,
    }
    # Configure the factory to return our mock loader
    mock_requests_loader_factory.return_value = mock_inner_loader

    with patch("socket.gethostbyname", return_value="8.8.8.8"):
        # Re-create the loader now that the factory is mocked correctly
        loader = create_document_loader()
        result = loader(url)
        assert result["document"] == expected_doc

    # Check that the inner loader was called
    mock_inner_loader.assert_called_once()

