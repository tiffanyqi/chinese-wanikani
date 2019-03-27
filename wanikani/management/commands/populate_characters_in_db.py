import json
import re

from django.core.management.base import BaseCommand
from django.db.utils import DataError

from wanikani.models import BaseCharacter

class Command(BaseCommand):
    """
    Takes all the character data from characters.json and creates a BaseCharacter
    object for each one.
    """
    def handle(self, *args, **options):
        with open('wanikani/static/data/characters.json', 'r') as f:
          data = json.load(f)
          for character in data:
            character_obj = data[character]
            required_keys = ['definition', 'frequency', 'hsk_level', 'pinyin']
            if all(key in character_obj for key in required_keys):
                definitions = json.dumps(character_obj.get('definition'))
                pinyin = json.dumps(character_obj.get('pinyin'))
                hsk_level = character_obj.get('hsk_level')
                frequency = character_obj.get('frequency')
                BaseCharacter.objects.update_or_create(
                    definitions=definitions,
                    character=character,
                    pinyin=pinyin,
                    hsk_level=hsk_level,
                    frequency=frequency
                )
            else:
                print('this character object does not contain some keys. please update or remove from characters.json {} {}'.format(character, character_obj))
