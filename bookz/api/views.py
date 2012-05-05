from importer import isbndb_importer
from django.http import HttpResponse, Http404
from tools import isbntools
from api.models import Apikey

def import_by_isbn(request, apikey, isbn):
    """import a book using a foreign api lookup on an isbn"""
    try:
        api = Apikey.objects.get(key=apikey)
        if not api.user.is_staff and api.active:
            raise Exception("API Key not valid")
        if isbntools.valid_isbn13(isbn):
            isbndb_importer.do_import(isbntools.strip(isbn))
        else:
            isbndb_importer.do_import(isbntools.convert(isbn))
    except Exception:
        return HttpResponse('False')
    else:
        return HttpResponse('True')
