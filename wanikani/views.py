from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from wanikani.models import BaseCharacter, User


def index(request):
    try:
        user = User.objects.get(email=request.user.email)
        context = {
            'characters': BaseCharacter.objects.filter(user_level=1),
            'user': user,
        }
        return render(request, 'wanikani/index.html', context)
    except:
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
