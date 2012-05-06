from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm
from django import forms
from django.template.defaultfilters import slugify

class Author(models.Model):
    """ a book has at least one author"""
    author_id = models.SlugField(verbose_name=_("Author ID"), primary_key=True)
    name = models.CharField(max_length=200, verbose_name=_("Author Name"))
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ("name",)

class Publisher(models.Model):
    """every book has exactly one Publisher"""
    publisher_id = models.SlugField(verbose_name=_("Publisher ID"), primary_key=True)
    name = models.CharField(max_length=200, verbose_name=_("Publisher Name"))
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

class PublisherForm(ModelForm):
    class Meta:
        model = Publisher
        fields = ("name",)

class Subject(models.Model):
    """a book can cover several subjects"""
    subject_id = models.SlugField(verbose_name=_("Subject ID"), primary_key=True)
    name = models.CharField(max_length=200, verbose_name=_("Subject Name"))
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

class SubjectForm(ModelForm):
    class Meta:
        model = Subject
        fields = ("name",)

class Book(models.Model):
    """a book, identified by it's ISBN-13"""
    isbn = models.IntegerField(verbose_name=_("ISBN-13"), primary_key=True)
    title = models.CharField(max_length=200, verbose_name=_("Title"))
    long_title = models.CharField(max_length=200, verbose_name=_("Long title"))
    authors = models.ManyToManyField(Author, verbose_name=_("Authors"))
    subjects = models.ManyToManyField(Subject, verbose_name=_("Subjects"), blank=True, null=True)
    publisher = models.ForeignKey(Publisher, verbose_name=_("Publisher"))
    ddc = models.CharField(max_length=10, verbose_name=_("Dewey Decimal Classification"), blank=True)
    language = models.CharField(max_length=50, verbose_name=_("Language"))
    edition_info = models.CharField(max_length=200, verbose_name=_("Edition Information"), blank=True)
    summary = models.TextField(blank=True, verbose_name=_("Summary of the Book"))
    cover = models.ImageField(upload_to="static/images/bookcovers/", verbose_name=_("Book cover image"), blank=True)
    created = models.DateTimeField(auto_now_add=True)

        
    def save(self, *args, **kwargs):
        """sets blank fields to '', sets long title if not given, then saves the book"""
        if not self.long_title:
            self.long_title = self.title
        if not self.ddc:
            self.ddc=''
        if not self.edition_info:
            self.edition_info=''
        if not self.summary:
            self.summary=''
        if not self.cover:
            self.cover = 'static/images/bookcovers/default.png'
        super(Book, self).save(*args, **kwargs)

    def __unicode__(self):
        return "%s [%s]" % (self.title, self.isbn)

class BookForm(ModelForm):
    def __init__(self,*args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        for monkey in ('publisher', 'authors', 'subjects'):
            self.fields[monkey].required = False  # monkeypatch requirements, because we may override them below
    subject_alt = forms.CharField(label=_("You can specify subjects which are not in list, one per line"), widget=forms.Textarea, required=False)
    authors_alt = forms.CharField(label=_("You can specify authors which are not in list, one per line"), widget=forms.Textarea, required=False)
    publisher_alt = forms.CharField(label=_("You can specify a publicher which is not in list"), required=False)
    class Meta:
        model = Book
    def clean(self):
        subjects = []
        for subject in self.cleaned_data.get('subject_alt',[]).splitlines():
            subjectdata = (slugify(subject), subject)
            if not subjectdata[0]:
                continue
            try:
                subject = Subject.objects.get(subject_id=subjectdata[0])
            except Subject.DoesNotExist:
                subject = Subject(subject_id=subjectdata[0], name=subjectdata[1])
                subject.save()
            subjects.append(subject)
        self.cleaned_data['subjects'] = list(self.cleaned_data.get('subjects',[])) + subjects
        print self.cleaned_data['subjects']
        
        authors = []
        for author in self.cleaned_data.get('authors_alt',[]).splitlines():
            authordata = (slugify(author), author)
            if not authordata[0]:
                continue
            try:
                author = Author.objects.get(author_id=authordata[0])
            except Author.DoesNotExist:
                author = Author(author_id=authordata[0], name=authordata[1])
                author.save()
            authors.append(author)
        self.cleaned_data['authors'] = list(self.cleaned_data.get('authors',[])) + authors
        print self.cleaned_data['authors']
        publisher = self.cleaned_data.get('publisher_alt',[]).strip()
        if publisher:
            try:
                publisher = Publisher.objects.get(publisher_id=slugify(publisher))
            except Publisher.DoesNotExist:
                publisher = Publisher(publisher_id=slugify(publisher), name=publisher)
                publisher.save()
            self.cleaned_data['publisher'] = publisher

        return super(BookForm, self).clean()
