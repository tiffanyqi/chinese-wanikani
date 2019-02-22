import datetime
import json

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from wanikani.models import BaseCharacter, ProgressCharacter, User
from wanikani.session.util import check_level_up, get_level, get_upcoming_review_date, level_up

@login_required
def review_view(request):
    """
    Begins a review session.
    """
    return render(request, 'wanikani/session/review.html')


@login_required
def learn_view(request):
    """
    Begins a learn session.
    """
    return render(request, 'wanikani/session/learn.html',)


@login_required
def summary_view(request):
    """
    Displays a summary from the previous review or learn.
    """
    user = User.objects.get(username=request.user.username)
    last_characters_reviewed = (ProgressCharacter.objects.filter(user=user)
        .filter(last_session=user.last_session))
    correct_characters = last_characters_reviewed.filter(last_correct=True)
    incorrect_characters = last_characters_reviewed.filter(last_correct=False)
    context = {
        'correct_characters': correct_characters,
        'incorrect_characters': incorrect_characters,
        'last_session': user.last_session,
    }
    return render(request, 'wanikani/session/summary.html', context)


@require_http_methods(['GET'])
def get_characters_to_review(request):
    if request.method == 'GET':
        return JsonResponse(characters_to_review(request.user), safe=False)

def characters_to_review(user):
    user = User.objects.get(username=user.username)
    now = datetime.datetime.now()
    results = (ProgressCharacter.objects.filter(user=user)
        .filter(Q(last_reviewed_date__isnull=False))
        .filter(Q(upcoming_review_date__lte=now) | Q(upcoming_review_date__isnull=True)))
    return [model.to_json() for model in results]


@require_http_methods(['GET'])
def get_characters_to_learn(request):
    if request.method == 'GET':
        return JsonResponse(characters_to_learn(request.user), safe=False)

def characters_to_learn(user):
    user = User.objects.get(username=user.username)
    results = (ProgressCharacter.objects.filter(user=user)
        .filter(Q(last_reviewed_date__isnull=True)))
    return [model.to_json() for model in results]


@require_http_methods(['POST'])
def update_learned_character(request):
    if request.method == 'POST':
        return JsonResponse(set_character_learned(
            request.POST.get('character'),
            json.loads(request.POST.get('is_complete')),
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

@require_http_methods(['POST'])
def update_reviewed_character(request):
    if request.method == 'POST':
        return JsonResponse(update_character(
            json.loads(request.POST.get('both_correct')),
            request.POST.get('character'),
            json.loads(request.POST.get('is_complete')),
            json.loads(request.POST.get('is_correct')),
            request.POST.get('type'),
            request.user,
            json.loads(request.POST.get('session_number')),
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

    if is_correct:
        character_object.last_correct = True
        character_object.num_correct[type] += 1
    else:
        character_object.last_correct = False
        character_object.num_current_incorrect[type] += 1

    if both_correct:
        new_level = get_level(character_object)
        character_object.num_correct['all'] += 1
        character_object.last_reviewed_date = now
        character_object.upcoming_review_date = get_upcoming_review_date(now, new_level)
        character_object.level = new_level
        character_object.num_current_incorrect['pinyin'] = 0
        character_object.num_current_incorrect['definitions'] = 0
        character_object.last_session = session_number
        user_object.last_session = session_number

    character_object.save()
    if check_level_up(user_object):
        level_up(user_object)
    return character_object.to_json()
