from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as log_in
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from wanikani.forms import SignUpForm
from wanikani.models import User


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            user_object = User.objects.create(
                username=username,
                password=raw_password,
                email=form.cleaned_data.get('email'),
                level=1,
            )
            user_object.save()
            # create level character objects
            log_in(request, user)
            return HttpResponseRedirect('/')

    else:
        form = SignUpForm()

    return render(request, 'wanikani/registration/signup.html', {'form': form})

def login_view(request):
    log_in(request)
    return HttpResponseRedirect('/')

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')
