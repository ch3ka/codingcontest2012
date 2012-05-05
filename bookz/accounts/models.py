from django.db import models
from django.contrib.auth.models import User, UserManager
from book.models import Book

class Profile(User):
    avatar = models.ImageField(upload_to="static/images/avatars/")
    objects = UserManager()

class Review(models.Model):
    book = models.ForeignKey(Book)
    user = models.ForeignKey(Profile)
    text = models.TextField()
    rating = models.SmallIntegerField(choices=((1,'*'),(2,'**'),(3,'***'),(4,'****'),(5,'*****')))

class Comment(models.Model):
    review = models.ForeignKey(Review)
    user = models.ForeignKey(Profile)
    text = models.TextField()
    rating = models.SmallIntegerField(choices=((1,'*'),(2,'**'),(3,'***'),(4,'****'),(5,'*****')))
