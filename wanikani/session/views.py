import datetime
import json

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from wanikani.models import BaseCharacter, ProgressCharacter, User
from wanikani.session.util import check_level_up, get_level, get_upcoming_review_date, level_up


@require_http_methods(['GET'])
def characters(request):
    if request.method == 'GET':
        results = list(BaseCharacter.objects.exclude(user_level=0).order_by('user_level'))
        return JsonResponse([model.to_json() for model in results], safe=False)


@require_http_methods(['GET'])
def character(request, character):
    """
    Provides more information on a single character
    """
    if request.method == 'GET':
        char = BaseCharacter.objects.get(character=character)
        return JsonResponse(char.to_json(), safe=False)


## CHARACTERS TO LEARN REQUESTS

@require_http_methods(['GET'])
def characters_to_learn(request):
    if request.method == 'GET':
        user = User.objects.get(username=request.user.username)
        now = datetime.datetime.now()
        results = (ProgressCharacter.objects
                .filter(user=user)
                .filter(upcoming_review_date__isnull=True)
        )
        return JsonResponse([model.to_json() for model in results], safe=False)


@require_http_methods(['POST'])
def update_learned_character(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        return JsonResponse(set_character_learned(
            body.get('character'),
            body.get('is_complete'),
            request.user,
        ), safe=False)


def set_character_learned(character, is_complete, user):
    now = datetime.datetime.now()
    base_character = BaseCharacter.objects.get(character=character)
    user_object = User.objects.get(username=user.username)
    character_object = ProgressCharacter.objects.get(character=base_character, user=user_object)

    if is_complete:
        new_level = get_level(character_object)
        character_object.upcoming_review_date = get_upcoming_review_date(now, new_level)
        character_object.save()
        return character_object.to_json()


## CHARACTERS TO REVIEW REQUESTS

@require_http_methods(['GET'])
def characters_to_review(request):
    if request.method == 'GET':
        user = User.objects.get(username=request.user.username)
        now = datetime.datetime.now()
        results = (ProgressCharacter.objects
                .filter(user=user)
                .filter(Q(upcoming_review_date__lte=now))
        )
        return JsonResponse([model.to_json() for model in results], safe=False)


@require_http_methods(['POST'])
def update_reviewed_character(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        return JsonResponse(update_character(
            body.get('both_correct'),
            body.get('character'),
            body.get('is_complete'),
            body.get('is_correct'),
            body.get('type'),
            request.user,
            body.get('session_number'),
        ), safe=False)

def update_character(both_correct, character, is_complete, is_correct, type, user, session_number):
    """
    Updates the character whether the user got the question right or wrong.

    Data is composed of the following:
    :both_correct - when the user has answered both pinyin and definition correctly
    :character - the character for the input
    :is_complete - when the user answered both pinyin and definition correctly at some point
    :is_correct - when the user's input is correct
    :type - whether the input is for pinyin or definition
    :session_number - what session number the character should be
    """
    now = datetime.datetime.now()
    base_character = BaseCharacter.objects.get(character=character)
    user_object = User.objects.get(username=user.username)
    character_object = ProgressCharacter.objects.get(character=base_character, user=user_object)
    if is_complete:
        character_object.num_times_shown += 1
        character_object.last_reviewed_date = now
        character_object.upcoming_review_date = get_upcoming_review_date(now, new_level)
        character_object.level = new_level
        character_object.last_session = session_number
        user_object.last_session = session_number

    if is_correct:
        character_object.last_correct = True
        character_object.num_correct[type] += 1
    else:
        character_object.last_correct = False
        character_object.num_current_incorrect[type] += 1

    if both_correct:
        new_level = get_level(character_object)
        character_object.num_correct['all'] += 1

    character_object.save()
    user_object.save()
    if check_level_up(user_object):
        level_up(user_object)
    return character_object.to_json()


# CURRENT LEVEL CHARACTER REQUESTS

@require_http_methods(['GET'])
def characters_at_level(request):
    if request.method == 'GET':
        user = User.objects.get(username=request.user.username)
        results = BaseCharacter.objects.filter(user_level=user.level)
        return JsonResponse([model.to_json() for model in results], safe=False)


def last_characters_reviewed(user):
    return (ProgressCharacter.objects.filter(user=user)
        .filter(last_session=user.last_session))

@require_http_methods(['GET'])
def last_session_characters_correct(request):
    if request.method == 'GET':
        user = User.objects.get(username=request.user.username)
        results = last_characters_reviewed(user).filter(last_correct=False)
        return JsonResponse([model.to_json() for model in results], safe=False)

@require_http_methods(['GET'])
def last_session_characters_incorrect(request):
    if request.method == 'GET':
        user = User.objects.get(username=request.user.username)
        results = last_characters_reviewed(user).filter(last_correct=True)
        return JsonResponse([model.to_json() for model in results], safe=False)
