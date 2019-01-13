import json
import re

from django.core.management.base import BaseCommand
from django.db.utils import DataError

from wanikani.models import BaseCharacter

class Command(BaseCommand):

    def handle(self, *args, **options):
        with open('wanikani/static/data/data.json', 'r') as f:
          data = json.load(f)
          for character in data:
            character_obj = data[character]
            try:
                definitions = json.dumps(re.split(', |/', character_obj['definition']))
                pinyin = json.dumps(character_obj['pinyin'].split('/'))
                hsk_level = character_obj['hsk_level']
                frequency = character_obj['frequency']
                BaseCharacter.objects.get_or_create(
                    definitions=definitions,
                    character=character,
                    pinyin=pinyin,
                    hsk_level=hsk_level,
                    frequency=frequency
                )
            except KeyError as e:
                print(character, 'KeyError',  'key', e)
            except DataError as e:
                print(character, 'DataError', e)
