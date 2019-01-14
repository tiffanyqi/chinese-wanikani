from django.contrib.auth import authenticate
from django.contrib.auth import login as log_in
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from wanikani.forms import SignUpForm
from wanikani.models import BaseCharacter, User


def index(request):
    try:
        user = User.objects.get(email=request.user.email)
        context = {
            'characters': BaseCharacter.objects.filter(user_level=user.level),
            'user': user,
        }
        return render(request, 'wanikani/index.html', context)
    except User.DoesNotExist:
        return render(request, 'wanikani/index_logged_out.html')

def character(request, character):
    base_character = BaseCharacter.objects.get(character=character)
    context = {
        'character': base_character,
    }
    return render(request, 'wanikani/character.html', context)

def test(request):
    return render(request, 'wanikani/test.html')

@login_required
def logout_view(request):
    logout(request)
    return render(request, 'wanikani/index_logged_out.html')

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
