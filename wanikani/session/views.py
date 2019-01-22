import json

from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from wanikani.models import BaseCharacter, LevelCharacter, User


def get_tested_characters(user):
    user = User.objects.get(email=user.email)
    results = BaseCharacter.objects.filter(
        user_level=user.level,
    ).order_by('user_level')
    return [model.to_json() for model in results]

# API #
@require_http_methods(['GET'])
def test_characters(request):
    if request.method == 'GET':
        return JsonResponse(get_tested_characters(request.user), safe=False)
