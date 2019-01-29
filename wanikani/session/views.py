import datetime
import json

from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from wanikani.models import BaseCharacter, ProgressCharacter, User
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
def post_updated_character(request):
    print(request)
    if request.method == 'POST':
        return JsonResponse(update_character(
            request.POST.get('both_correct'),
            request.POST.get('character'),
            request.POST.get('is_complete'),
            request.POST.get('is_correct'),
            request.POST.get('type'),
            request.user,
        ), safe=False)

def update_character(both_correct, character, is_complete, is_correct, type, user):
    """
    Updates the character whether the user got the question right or wrong.

    Data is composed of the following:
    :both_correct - when the user has answered both pinyin and definition correctly
    :character - the character for the input
    :is_complete - when the user answered both pinyin and definition correctly at some point
    :is_correct - when the user's input is correct
    :type - whether the input is for pinyin or definition
    """
    now = datetime.datetime.now()
    base_character = BaseCharacter.objects.get(character=character)
    user_object = User.objects.get(username=user.username)
    character_object = ProgressCharacter.objects.get(character=base_character, user=user_object)
    if is_complete:
        character_object.num_times_shown += 1

    if is_correct:
        character_object.num_correct[type] += 1
    else:
        character_object.num_current_incorrect[type] += 1

    if both_correct:
        new_level = get_level(character_object)
        character_object.num_correct['all'] += 1
        character_object.last_reviewed_date = now
        character_object.upcoming_review_date = get_upcoming_review_date(now, new_level)
        character_object.level = new_level
        character_object.num_current_incorrect['pinyin'] = 0
        character_object.num_current_incorrect['definitions'] = 0

    character_object.save()
    return character_object.to_json()
