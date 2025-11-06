from pyld import jsonld

from .._jsonld import create_document_loader

jsonld.set_document_loader(create_document_loader())
