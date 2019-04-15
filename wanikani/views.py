import datetime
import json

from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods

from wanikani.models import BaseCharacter, ProgressCharacter, User


@ensure_csrf_cookie
def home(request):
    return render(request, 'wanikani/new-base.html')


@require_http_methods(['GET'])
def user(request):
    if request.method == 'GET':
        user = User.objects.get(username=request.user.username)
        return JsonResponse(user.to_json(), safe=False)


@require_http_methods(['GET'])
def characters(request):
    if request.method == 'GET':
        results = list(BaseCharacter.objects.exclude(user_level=0).order_by('user_level'))
        return JsonResponse([model.to_json() for model in results], safe=False)


# TODO: consolidate this with session/views.py
@require_http_methods(['GET'])
def character(request, character):
    """
    Provides more information on a single character
    """
    if request.method == 'GET':
        char = BaseCharacter.objects.get(character=character)
        return JsonResponse(char.to_json(), safe=False)


@require_http_methods(['GET'])
def characters_to_learn(request):
    if request.method == 'GET':
        user = User.objects.get(username=request.user.username)
        now = datetime.datetime.now()
        results = (ProgressCharacter.objects
                .filter(user=user)
                .filter(last_reviewed_date__isnull=True, upcoming_review_date__isnull=False)
        )
        return JsonResponse([model.to_json() for model in results], safe=False)

@require_http_methods(['GET'])
def characters_to_review(request):
    if request.method == 'GET':
        user = User.objects.get(username=request.user.username)
        now = datetime.datetime.now()
        results = (ProgressCharacter.objects
                .filter(user=user)
                .filter(Q(last_reviewed_date__isnull=False))
                .filter(Q(upcoming_review_date__lte=now) | Q(upcoming_review_date__isnull=True))
        )
        return JsonResponse([model.to_json() for model in results], safe=False)


@require_http_methods(['GET'])
def characters_at_level(request):
    if request.method == 'GET':
        user = User.objects.get(username=request.user.username)
        results = BaseCharacter.objects.filter(user_level=user.level)
        return JsonResponse([model.to_json() for model in results], safe=False)
