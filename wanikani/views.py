import json

from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from wanikani.models import BaseCharacter, LevelCharacter, User


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
        return render(request, 'wanikani/index.html')

@login_required
def characters(request):
    """
    Displays all characters
    """
    context = {
        'characters': list(BaseCharacter.objects.exclude(user_level=0).order_by('user_level')),
    }
    return render(request, 'wanikani/characters.html', context)

@login_required
def character(request, character):
    """
    Provides more information on a single character
    """
    context = {
        'character': BaseCharacter.objects.get(character=character),
    }
    return render(request, 'wanikani/character.html', context)

@login_required
def session(request):
    """
    Begin a session of either a lesson or a review.
    """
    return render(request, 'wanikani/session.html')
