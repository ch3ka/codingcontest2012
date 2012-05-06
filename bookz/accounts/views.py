from django.contrib import auth
from django import forms
from accounts.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    return render_to_response("accounts/own_profile.html", 
        {},
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

