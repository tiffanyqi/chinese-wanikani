import json

from django.core.management.base import BaseCommand

from wanikani.models import BaseCharacter

class Command(BaseCommand):

    def handle(self, *args, **options):
        hsk_levels = 6
        current_hsk_level = 1
        current_user_level = 1
        num_characters_in_user_level = 43
        character_number = 0
        for i in range(current_hsk_level, hsk_levels+1):
            level_characters = BaseCharacter.objects.filter(hsk_level=i).order_by('frequency')
            for character in level_characters:
                if character_number == num_characters_in_user_level:
                    current_user_level += 1
                    character_number = 0
                else:
                    character.user_level = current_user_level
                    character.save()
                    character_number += 1
