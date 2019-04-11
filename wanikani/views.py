import datetime
import json

from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from wanikani.models import BaseCharacter, ProgressCharacter, User


def index(request):
    """
    Displays the user's dashboard or the logged out page
    """
    try:
        user = User.objects.get(username=request.user.username)
        now = datetime.datetime.now()
        context = {
            'characters': BaseCharacter.objects.filter(user_level=user.level),
            'characters_to_learn': (ProgressCharacter.objects
                .filter(user=user)
                .filter(Q(last_reviewed_date__isnull=True))
                .count()),
            'characters_to_review': (ProgressCharacter.objects
                .filter(user=user)
                .filter(Q(last_reviewed_date__isnull=False))
                .filter(Q(upcoming_review_date__lte=now) | Q(upcoming_review_date__isnull=True))
                .count()),
            'user': user,
        }
        return render(request, 'wanikani/dashboard.html', context)
    except User.DoesNotExist:
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

def test(request):
    return render(request, 'wanikani/test.html')


@require_http_methods(['GET'])
def get_user(request):
    if request.method == 'GET':
        return JsonResponse(user(request.user), safe=False)

def user(user):
    user = User.objects.get(username=user.username)
    return user.to_json()
