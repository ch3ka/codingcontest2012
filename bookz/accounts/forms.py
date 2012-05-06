from django import forms
from accounts.models import User, Review, Comment
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
 
class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    avatar = forms.ImageField(required=False)
 
    class Meta:
        model = User
        fields = ("username", "email", "avatar", "password1", "password2",)
 
    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.avatar = self.cleaned_data["avatar"]
        if commit:
            user.save()
        return user

class EditUserForm(ModelForm):
    class Meta:
        model = User
        fields = ("website", "bio", "avatar")

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        exclude = ("book", "user")

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ("review", "user")
