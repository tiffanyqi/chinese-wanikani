from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'wanikani/index.html')

def character(request, character):
    context = {
        'character': character,
    }
    return render(request, 'wanikani/character.html', context)
