from django.contrib import auth
from django import forms
from accounts.forms import UserCreationForm, EditUserForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from accounts.models import User, Comment, Review

@login_required
def own_profile(request):
    if request.method == "POST":
        form = EditUserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
    else:
        form = EditUserForm(instance=request.user)
    return render_to_response("accounts/own_profile.html", 
        {'form': form},
        context_instance=RequestContext(request)
    )

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/loggedin")
    else:
        form = UserCreationForm()
    return render_to_response("registration/register.html", {
        'form': form,},
        context_instance=RequestContext(request)
    )

def profile(request, user):
    user = User.objects.get(username=user)
    return render_to_response("accounts/profile.html", {
        'user': user,
        'comments': Comment.objects.filter(user=user),
        'reviews': Review.objects.filter(user=user),
        },
        context_instance=RequestContext(request)
    )
