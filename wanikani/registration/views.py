from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as log_in
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from wanikani.forms import SignUpForm

from wanikani.registration.util import save_user, setup_characters


def signup(request):
    """
    Signs up a user.
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')

            user = authenticate(username=username, password=password)
            user_object = save_user(username, password, email)
            setup_characters(user_object)
            log_in(request, user)
            return HttpResponseRedirect('/')

    else:
        form = SignUpForm()

    return render(request, 'wanikani/registration/signup.html', {'form': form})

def login_view(request):
    """
    Logs in a user.
    """
    log_in(request)
    return HttpResponseRedirect('/')

@login_required
def logout_view(request):
    """
    Logs out a user.
    """
    logout(request)
    return HttpResponseRedirect('/')
