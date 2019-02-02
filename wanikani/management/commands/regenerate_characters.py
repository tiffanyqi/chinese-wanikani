import json

from django.core.management.base import BaseCommand

from wanikani.models import BaseCharacter, ProgressCharacter, User
from wanikani.registration.util import setup_characters

class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.get(username='newuser9') # test account
        ProgressCharacter.objects.filter(user=user).delete()
        setup_characters(user)
