from django.db import models
from accounts.models import Profile

class Apikey(models.Model):
    user = models.ForeignKey(Profile)
    key = models.CharField(max_length=40, primary_key=True)
    active = models.BooleanField(default=True)
