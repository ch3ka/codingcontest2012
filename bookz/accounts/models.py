from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, UserManager
from book.models import Book

class User(User):
    avatar = models.ImageField(upload_to="static/images/avatars/", blank=True)
    owns = models.ManyToManyField(Book, related_name="whoowns", blank=True, null=True)
    read = models.ManyToManyField(Book, related_name="whoread", blank=True, null=True)
    website = models.CharField(blank=True, max_length=200)
    bio = models.TextField(blank=True)
    objects = UserManager()

    def save(self, *args, **kwargs):
        '''sanitizes avatar before saving'''
        if not self.avatar:
            self.avatar = 'static/images/avatars/default.jpg'
        super(User, self).save(*args, **kwargs)

class Review(models.Model):
    book = models.ForeignKey(Book)
    user = models.ForeignKey(User)
    text = models.TextField(verbose_name=_("Your review text"))
    created = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(choices=((1,'*'),(2,'**'),(3,'***'),(4,'****'),(5,'*****')), verbose_name=_("Your rating of the book"))
    def rating_as_range(self):
        return range(self.rating)

class Comment(models.Model):
    review = models.ForeignKey(Review)
    user = models.ForeignKey(User)
    text = models.TextField(verbose_name=_("Your comment"))
    created = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(choices=((1,'*'),(2,'**'),(3,'***'),(4,'****'),(5,'*****')), verbose_name=_("Your rating of the review"))
    def rating_as_range(self):
        return range(self.rating)
