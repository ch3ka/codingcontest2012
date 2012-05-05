from django.db import models
from accounts.models import User

class Apikey(models.Model):
    user = models.ForeignKey(User)
    key = models.CharField(max_length=40, primary_key=True)
    active = models.BooleanField(default=True)
