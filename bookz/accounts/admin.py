from django.contrib import admin
from accounts.models import User, Review, Comment

admin.site.register(User)
admin.site.register(Review)
admin.site.register(Comment)

