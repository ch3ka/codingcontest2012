from api.decorators import booleanapicall, keyrequired
import api.internal as internalapi

@booleanapicall
def import_by_isbn(request, isbn, user):
    """import a book using a foreign api lookup on an isbn"""
    internalapi.import_by_isbn(isbn)

@booleanapicall
def mark_as_owned(request, isbn, user):
    internalapi.mark_as_owned(isbn, user)

@booleanapicall
def mark_as_read(request, isbn, user):
    internalapi.mark_as_read(isbn, user)
