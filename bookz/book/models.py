from django.db import models
from django.utils.translation import ugettext_lazy as _

class Author(models.Model):
    """ a book has at least one author"""
    author_id = models.SlugField(verbose_name=_("Author ID"), primary_key=True)
    name = models.CharField(max_length=200, verbose_name=_("Author Name"))

    def __unicode__(self):
        return self.name

class Publisher(models.Model):
    """every book has exactly one Publisher"""
    publisher_id = models.SlugField(verbose_name=_("Publisher ID"), primary_key=True)
    name = models.CharField(max_length=200, verbose_name=_("Publisher Name"))

    def __unicode__(self):
        return self.name

class Subject(models.Model):
    """a book can cover several subjects"""
    subject_id = models.SlugField(verbose_name=_("Subject ID"), primary_key=True)
    name = models.CharField(max_length=200, verbose_name=_("Subject Name"))

    def __unicode__(self):
        return self.name

class Book(models.Model):
    """a book, described by it's ISBN-13"""
    isbn = models.IntegerField(verbose_name=_("ISBN-13"), primary_key=True)
    title = models.CharField(max_length=200, verbose_name=_("Title"))
    long_title = models.CharField(max_length=200, verbose_name=_("Long title"))
    authors = models.ManyToManyField(Author, verbose_name=_("Authors"))
    subjects = models.ManyToManyField(Subject, verbose_name=_("Subjects"), blank=True, null=True)
    publisher = models.ForeignKey(Publisher, verbose_name=_("Publisher"))
    ddc = models.CharField(max_length=10, verbose_name=_("Dewey Decimal Classification"), blank=True)
    language = models.CharField(max_length=50, verbose_name=_("Language"))
    edition_info = models.CharField(max_length=200, verbose_name=_("Edition Information"), blank=True)
    summary = models.TextField(blank=True)

        
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
        super(Book, self).save(*args, **kwargs)

    def __unicode__(self):
        return "%s [%s]" % (self.title, self.isbn)
