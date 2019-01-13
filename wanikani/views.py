from django.http import HttpResponse
from django.shortcuts import render

from wanikani.models import BaseCharacter


def index(request):
    return render(request, 'wanikani/index.html')

def character(request, character):
    base_character = BaseCharacter.objects.get(character=character)
    context = {
        'character': base_character,
    }
    return render(request, 'wanikani/character.html', context)
