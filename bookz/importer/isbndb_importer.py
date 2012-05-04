from django.conf import settings
from BeautifulSoup import BeautifulStoneSoup, Tag, NavigableString

import urllib2 as urllib
import importer.generic

API_URL = "http://isbndb.com/api/books.xml?access_key=%(APIKEY)s&index1=isbn&value1=%%(ISBN)s" \
          "&results=details&results=subjects&results=authors&results=texts" % {'APIKEY': settings.ISBNDB_APIKEY}

def do_import(isbn13):
    xml = urllib.urlopen(API_URL % {'ISBN': isbn13}).read()
    soup = BeautifulStoneSoup(xml)
    print soup.prettify()
    book = soup.isbndb.booklist.bookdata
    print book.prettify()
    data = {
            'isbn': isbn13,
            'title': book.title.string,
            'long_title': book.titlelong.string,
            'edition_info': book.details['edition_info'],
            'language': book.details['language'],
            'ddc': book.details['dewey_decimal_normalized'],
            'summary': book.summary.string,
            'subjects': [(subject['subject_id'], subject.string) for subject in book.subjects.contents if subject != '\n'],
            'authors': [(person['person_id'], person.string) for person in book.authors.contents if person != '\n'],
            'publisher': (book.publishertext['publisher_id'], book.publishertext.string),
            }
    importer.generic.do_import(data)
