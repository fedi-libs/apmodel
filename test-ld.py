from apmodel.core.object import Object
from pyld import jsonld
from pyld.documentloader import requests


def myloader(*args, **kwargs):
    requests_loader = requests.requests_document_loader(*args, **kwargs)

    def loader(url, options={}):
        options["headers"]["Accept"] = "application/ld+json;profile=http://www.w3.org/ns/json-ld#context, application/ld+json, application/json;q=0.5, text/html;q=0.8, application/xhtml+xml;q=0.8"
        return requests_loader(url, options)

    return loader


jsonld.set_document_loader(myloader())
expanded = jsonld.expand({
    "@context": "https://www.w3.org/ns/activitystreams",
    "id": "http://example.org/foo",
    "type": "Object",
    "name": "A Simple Note",
    "content": "This is a simple note",
})
print(expanded[0])
Object.model_validate(expanded[0])