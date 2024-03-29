from django.shortcuts import render_to_response
from django.template import RequestContext
from book.models import Book, BookForm, ISBNBookForm, Author, AuthorForm, Subject, SubjectForm, Publisher, PublisherForm
from accounts.models import Review, Comment
from accounts.forms import ReviewForm, CommentForm
from api import internal as internalapi
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect 

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
    book = Book.objects.get(isbn=isbn)
    reviews = Review.objects.filter(book=book).order_by("-created")
    for review in reviews:
        review.comments = Comment.objects.filter(review=review)
    return render_to_response('book.html',
        {'book': book,'reviews': reviews},
        context_instance=RequestContext(request)
    )

def editbook(request, isbn):
    book = Book.objects.get(isbn=isbn)
    if request.method == "POST" and request.user.is_authenticated():
        form = BookForm(request.POST, request.FILES, instance = book)
        if form.is_valid():
            form.save()
    else:
        form = BookForm(instance = book)

    return render_to_response('editbook.html', 
        {'book': book, 'form': form},
        context_instance=RequestContext(request)
    )

@login_required
def ownbook(request, isbn):
    internalapi.mark_as_owned(isbn, request.user)
    return HttpResponseRedirect('/accounts/profiles/'+request.user.username)

@login_required
def readbook(request, isbn):
   internalapi.mark_as_read(isbn, request.user)
   return HttpResponseRedirect('/accounts/profiles/'+request.user.username)

@login_required
def comment(request, reviewid):
    if request.method == "POST":
        comment = Comment(user=request.user, review=Review.objects.get(pk=reviewid))
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            isbn = Review.objects.get(pk=reviewid).book.isbn
            return HttpResponseRedirect('/book/'+str(isbn))
    else:
        form = CommentForm()
    return render_to_response('comment.html',
        {'form': form,
         'review': Review.objects.get(pk=reviewid),
        },
        context_instance=RequestContext(request)
    )

@login_required
def addbookbyisbn(request):
    from tools import isbntools
    isbnform = ISBNBookForm(request.POST)
    if isbnform.is_valid():
        try:
            internalapi.import_by_isbn(isbnform.cleaned_data['isbn'])
        except Exception:
            return HttpResponse("something went wrong. could not import data for ISBN %s" % isbnform.cleaned_data['isbn'])
        else:
            return HttpResponseRedirect("/book/edit/"+isbntools.strip(isbnform.cleaned_data['isbn']))

@login_required
def addbook(request):
    from tools import isbntools
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            return HttpResponseRedirect('/book/'+isbntools.strip(str(form.cleaned_data['isbn'])))
    else:
        form = BookForm()
    return render_to_response('addbook.html',
        {'form': form, 'isbnform': ISBNBookForm(request.POST)},
        context_instance=RequestContext(request)
    )

@login_required
def reviewbook(request, isbn):
    if request.method == "POST":
        review = Review(user=request.user, book=Book.objects.get(isbn=isbn))
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/book/'+isbn)
    else:
        form = ReviewForm()
    return render_to_response('review.html',
        {'form': form},
        context_instance=RequestContext(request)
    )


def authors(request):
    return render_to_response('authors.html', 
        {'authors': Author.objects.all()},
        context_instance=RequestContext(request)
    )

def author(request, author_id):
    author = Author.objects.get(author_id=author_id)
    if request.method == "POST" and request.user.is_authenticated():
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
    else:
        form = AuthorForm(instance=author)
    return render_to_response('author.html', 
        {'author': author,
         'books': Book.objects.filter(authors__author_id=author_id),
         'form': form
        },
        context_instance=RequestContext(request)
    )

def publishers(request):
    return render_to_response('publishers.html', 
        {'publishers': Publisher.objects.all()},
        context_instance=RequestContext(request)
    )

def publisher(request, publisher_id):
    publisher = Publisher.objects.get(publisher_id=publisher_id)
    if request.method == "POST" and request.user.is_authenticated():
        form = PublisherForm(request.POST, instance=publisher)
        if form.is_valid():
            form.save()
    else:
        form = PublisherForm(instance=publisher)
    return render_to_response('publisher.html', 
        {'publisher': publisher,
         'books': Book.objects.filter(publisher__publisher_id=publisher_id),
         'form': form
        },
        context_instance=RequestContext(request)
    )

def subjects(request):
    return render_to_response('subjects.html', 
        {'subjects': Subject.objects.all()},
        context_instance=RequestContext(request)
    )

def subject(request, subject_id):
    subject = Subject.objects.get(subject_id=subject_id)
    if request.method == "POST" and request.user.is_authenticated():
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
    else:
        form = SubjectForm(instance=subject)
    return render_to_response('subject.html', 
        {'subject': subject,
         'books': Book.objects.filter(subjects__subject_id=subject_id),
         'form': form
        },
        context_instance=RequestContext(request)
    ) 

def setlang(request, lang):
    return render_to_response('setlang.html',{'lang': lang},
    context_instance=RequestContext(request)
    )
