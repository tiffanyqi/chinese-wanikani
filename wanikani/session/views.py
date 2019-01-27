import datetime
import json

from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from wanikani.models import ProgressCharacter, User


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
        character_object.num_correct['all'] += 1
        character_object.last_reviewed_date = now
        character_object.level += get_level(character_object)
        character_object.num_current_incorrect['pinyin'] = 0
        character_object.num_current_incorrect['definitions'] = 0
        character_object.upcoming_review_date = get_upcoming_review_date(now, character_object.level)

    character_object.save()
    return character_object.to_json()

def get_upcoming_review_date(now, level):
    """
    Wanikani's SRS system separates each level by the following hours: 4, 4, 16, 24, 48, 240, 384, 2160
    To make the logic a bit more simple, the hours here will increment by a multiple of 2, such as:
        2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048
    When the user passes the 11th level, it will be considered burned and removed from the queue.
    """
    base_hour = 2
    hours_from_now = base_hour ** level
    next_date = now + datetime.timedelta(hours=hours_from_now)
    return next_date.replace(microsecond=0, second=0, minute=0) # rounds down

def get_level(character):
    """
    There is also a penalty factor in which reduces the level further depending on how many times you answer
    incorrectly in a given session.
    """
    # TODO: add a penalty factor to further decrease the more times a user answers incorrectly
    if character.num_current_incorrect['pinyin'] > 0 or character.num_current_incorrect['definitions'] > 0:
        return character.level - 1
    else:
        return character.level + 1
