""" internal API. The functions listed here should in
general NOT catch exceptions, that's the job of the callers.
function names beginning with 'get_' should return a dict or a list,
whichever appliccable, other functions should return None and signal
errors with an Exception.
"""

from importer import isbndb_importer
from tools import isbntools
from book.models import Book

def import_by_isbn(isbn):
    if isbntools.valid_isbn13(isbn):
        isbndb_importer.do_import(isbntools.strip(isbn))
    else:
        isbndb_importer.do_import(isbntools.convert(isbn))

def mark_as_owned(isbn, user):
    user.owns.add(Book.objects.get(isbn=isbn))

def mark_as_read(isbn, user):
    user.read.add(Book.objects.get(isbn=isbn))

