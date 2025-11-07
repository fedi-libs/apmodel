import glob
import ipaddress
import json
import os
import socket
from functools import lru_cache
from typing import Callable
from urllib.parse import urlparse

from pyld import jsonld
from pyld.documentloader import requests

_PRELOADS_DIR = os.path.join(os.path.dirname(__file__), "_preloads")

PRELOAD_JSONLD_PATH_MAPPINGS = {}

if os.path.isdir(_PRELOADS_DIR):
    search_pattern = os.path.join(_PRELOADS_DIR, "*.jsonld")
    for file_path in glob.glob(search_pattern):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data_metadata = json.load(f)

            urls_to_map = data_metadata.get("urls")

            if isinstance(urls_to_map, list) and urls_to_map:
                for url in urls_to_map:
                    PRELOAD_JSONLD_PATH_MAPPINGS[url] = file_path
        except Exception:
            pass


@lru_cache(maxsize=100)
def get_schema(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        full_data = json.load(f)
        return full_data.get("schema", {})


#@lru_cache(maxsize=100)
def cached_loader(
    requests_loader: Callable[[str, dict], dict], url, options={}
):
    #options = json.loads(options_str)
    if "headers" not in options:
        options["headers"] = {}
    options["headers"]["Accept"] = (
        "application/ld+json;profile=http://www.w3.org/ns/json-ld#context, application/ld+json, application/json;q=0.5, text/html;q=0.8, application/xhtml+xml;q=0.8"
    )
    return requests_loader(url, options)


def create_document_loader(*args, **kwargs):
    requests_loader = requests.requests_document_loader(*args, **kwargs)

    def loader(url, options={}):
        if url in PRELOAD_JSONLD_PATH_MAPPINGS:
            file_path = PRELOAD_JSONLD_PATH_MAPPINGS[url]

            schema_doc = get_schema(file_path)

            return {
                "contextUrl": None,
                "documentUrl": url,
                "contentType": "application/ld+json",
                "document": schema_doc,
            }

        else:
            parsed_url = urlparse(url)
            hostname = parsed_url.hostname
            if hostname:
                try:
                    ip = ipaddress.ip_address(socket.gethostbyname(hostname))
                    if ip.is_private or ip.is_loopback:
                        raise jsonld.JsonLdError(
                            "Loading from local or private network is not allowed.",
                            "jsonld.LoadContextFailed",
                            {"url": url},
                        )
                except socket.gaierror:
                    raise jsonld.JsonLdError(
                        "Could not resolve hostname.",
                        "jsonld.LoadContextFailed",
                        {"url": url},
                    )

            
            #options_str = json.dumps(options, sort_keys=True)
            return cached_loader(requests_loader, url, options)

    return loader