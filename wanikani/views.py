from django.http import HttpResponse
from django.shortcuts import render

from wanikani.models import BaseCharacter


def index(request):
    # test user level
    context = {
        'characters': BaseCharacter.objects.filter(user_level=50),
        'user': request.user,
    }
    return render(request, 'wanikani/index.html', context)

def character(request, character):
    base_character = BaseCharacter.objects.get(character=character)
    context = {
        'character': base_character,
    }
    return render(request, 'wanikani/character.html', context)

def test(request):
    return render(request, 'wanikani/test.html')
