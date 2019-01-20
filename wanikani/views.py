import json

from django.contrib.auth import authenticate
from django.contrib.auth import login as log_in
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from wanikani.forms import SignUpForm
from wanikani.models import BaseCharacter, User


def index(request):
    """
    Displays the user's dashboard or the logged out page
    """
    try:
        user = User.objects.get(email=request.user.email)
        context = {
            'characters': BaseCharacter.objects.filter(user_level=user.level),
            'user': user,
        }
        return render(request, 'wanikani/dashboard.html', context)
    except AttributeError:
        return render(request, 'wanikani/index_logged_out.html')

@login_required
def characters(request):
    """
    All characters page
    """
    context = {
        'characters': list(BaseCharacter.objects.exclude(user_level=0).order_by('user_level')),
    }
    return render(request, 'wanikani/characters.html', context)

@login_required
def character(request, character):
    """
    Individual character page
    """
    base_character = BaseCharacter.objects.get(character=character)
    context = {
        'character': base_character,
    }
    return render(request, 'wanikani/character.html', context)

@login_required
def test(request):
    """
    Test a user's ability
    """
    user = User.objects.get(email=request.user.email)
    characters = (BaseCharacter.objects.filter(user_level=user.level)
        .values('character', 'definitions', 'pinyin'))
    context = {
        'characters': json.dumps(list(characters)),
    }
    return render(request, 'wanikani/test.html', context)

# Authentication #

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
            log_in(request, user)
            return HttpResponseRedirect('/')

    else:
        form = SignUpForm()

    return render(request, 'wanikani/signup.html', {'form': form})

def login_view(request):
    log_in(request)
    return HttpResponseRedirect('/')

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')
