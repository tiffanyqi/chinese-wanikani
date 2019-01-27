import datetime
import json

from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from wanikani.models import ProgressCharacter, User
from wanikani.session.util import get_level, get_upcoming_review_date


@require_http_methods(['GET'])
def get_user_level_characters(request):
    if request.method == 'GET':
        return JsonResponse(user_level_characters(request.user), safe=False)

def user_level_characters(user):
    user = User.objects.get(username=user.username)
    results = (ProgressCharacter.objects.filter(character__user_level=user.level, user=user)
        .order_by('character__user_level'))
    return [model.to_json() for model in results]


@require_http_methods(['POST'])
def post_updated_character(request, data):
    if request.method == 'POST':
        return JsonResponse(update_character(request.user, data), safe=False)

def update_character(user, data):
    """
    Updates the character whether the user got the question right or wrong.
    """
    now = datetime.datetime.now()
    character_object = ProgressCharacter.objects.get(character__character=data.character, user=user)
    if data.isComplete:
        character_object.num_times_shown += 1

    if data.isCorrect:
        character_object.num_correct[data.type] += 1
    else:
        character_object.num_current_incorrect[data.type] += 1

    if data.bothCorrect:
        current_level = character_object.level
        new_level = current_level + get_level(character_object)
        character_object.num_correct['all'] += 1
        character_object.last_reviewed_date = now
        character_object.upcoming_review_date = get_upcoming_review_date(now, new_level)
        character_object.level = new_level
        character_object.num_current_incorrect['pinyin'] = 0
        character_object.num_current_incorrect['definitions'] = 0

    character_object.save()
    return character_object.to_json()
