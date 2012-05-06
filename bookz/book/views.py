from django.shortcuts import render_to_response
from django.template import RequestContext
from book.models import Book, Author, Subject, Publisher

def index(request):
    return render_to_response('index.html', {},
        context_instance=RequestContext(request)
    )


def about(request):
    return render_to_response('about.html', {},
        context_instance=RequestContext(request)
    )

def books(request):
    return render_to_response('books.html', 
        {'books': Book.objects.all()},
        context_instance=RequestContext(request)
    )

def books_by(request, by, key):
    if by == 'author':
        books = Book.objects.filter(authors__author_id=key)
    if by == 'subject':
        books = Book.objects.filter(subjects__subject_id=key)
    if by == 'publisher':
        books = Book.objects.filter(publisher__publisher_id=key)
    return render_to_response('books.html', 
        {'books': books, 'by': by, 'key': key},
        context_instance=RequestContext(request)
    )

def book(request, isbn):
    return render_to_response('book.html', 
        {'book': Book.objects.get(isbn=isbn)},
        context_instance=RequestContext(request)
    )

def authors(request):
    return render_to_response('authors.html', 
        {'authors': Author.objects.all()},
        context_instance=RequestContext(request)
    )

def author(request, author_id):
    return render_to_response('author.html', 
        {'author': Author.objects.get(author_id=author_id)},
        context_instance=RequestContext(request)
    )

def publishers(request):
    return render_to_response('publishers.html', 
        {'publishers': Publisher.objects.all()},
        context_instance=RequestContext(request)
    )

def publisher(request, publisher_id):
    return render_to_response('publisher.html', 
        {'publisher': Publisher.objects.get(publisher_id=publisher_id)},
        context_instance=RequestContext(request)
    )

def subjects(request):
    return render_to_response('subjects.html', 
        {'subjects': Subject.objects.all()},
        context_instance=RequestContext(request)
    )

def subject(request, subject_id):
    return render_to_response('subject.html', 
        {'subject': Subject.objects.get(subject_id=subject_id)},
        context_instance=RequestContext(request)
    )
