from pyld import jsonld

from .._jsonld import preloaded_loader

jsonld.set_document_loader(preloaded_loader())
