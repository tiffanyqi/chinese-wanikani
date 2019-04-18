from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods

from wanikani.models import User


@ensure_csrf_cookie
def home(request):
    return render(request, 'wanikani/new-base.html')


@require_http_methods(['GET'])
def user(request):
    if request.method == 'GET':
        user = User.objects.get(username=request.user.username)
        return JsonResponse(user.to_json(), safe=False)
