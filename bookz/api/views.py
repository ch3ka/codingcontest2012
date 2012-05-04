from importer import isbndb_importer
from django.http import HttpResponse, Http404
from tools import isbntools

def import_by_isbn(request, isbn):
    """import a book using a foreign api lookup on an isbn"""
    try:
        if isbntools.valid_isbn13(isbn):
            isbndb_importer.do_import(isbntools.strip(isbn))
        else:
            isbndb_importer.do_import(isbntools.convert(isbn))
    except Exception:
        return HttpResponse('False')
    else:
        return HttpResponse('True')
