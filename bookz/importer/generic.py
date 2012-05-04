from book.models import Book, Author, Publisher, Subject

def do_import(data, if_book_exists='continue'):
    """import a book in the database. 
    
    Expects a dict of the following format:
{ 'publisher': (u'oreilly', u"Farnham ; O'Reilly, 2002 printing, c2003."), 'authors': [(u'ray_randy_j', u'Ray, Randy J.'), (u'kulchenko_pavel', u'Kulchenko, Pavel')], 'subjects': [(u'perl_computer_program_language', u'Perl (Computer program language)'), (u'internet_programming', u'Internet programming')], 'language': u'eng', 'title': u'Programming Web services with Perl', 'ddc': u'5.2762', 'long_title': None, 'edition_info': u'', 'summary': None }
    which other importers have to deliver.

    if_book_exists may be eighter one of 'continue', 'overwrite', 'error'
    """

    try:
        book = Book.objects.get(isbn=data['isbn'])
    except Book.DoesNotExist:
        book = Book(isbn=data['isbn'], title=data['title'], 
                    long_title=data.get('long_title'), language=data.get('language'), 
                    ddc=data.get('ddc'), edition_info=data.get('edition_info'), 
                    summary=data.get('summary'))  
        try:
            publisher = Publisher.objects.get(publisher_id=data['publisher'][0])
        except Publisher.DoesNotExist:
            publisher = Publisher(publisher_id=data['publisher'][0], name=data['publisher'][1])
            publisher.save()
        book.publisher = publisher

        for authordata in data['authors']:
            try:
                author = Author.objects.get(author_id=authordata[0])
            except Author.DoesNotExist:
                author = Author(author_id=authordata[0], name=authordata[1])
                author.save()
            book.authors.add(author)

        for subjectdata in data['subjects']:
            try:
                subject = Subject.objects.get(subject_id=subjectdata[0])
            except Subject.DoesNotExist:
                subject = Subject(subject_id=subjectdata[0], name=subjectdata[1])
                subject.save()
            book.subjects.add(subject)

        book.save()
    else:
        if if_book_exists.lower() == "error":
            raise ValueError("Book %s already exists!" % data['isbn'])
        elif if_book_exists.lower() == "overwrite":
            book.delete()
            do_import(data)
        elif if_book_exists.lower() != "continue":
            raise ValueError("if_book_exists must be eighter one of 'continue', 'overwrite', 'error'")
