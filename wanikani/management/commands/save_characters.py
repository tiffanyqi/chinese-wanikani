import json

from django.core.management.base import BaseCommand

from wanikani.models import BaseCharacter

class Command(BaseCommand):

    def handle(self, *args, **options):
        with open('wanikani/static/data/data.json', 'r') as f:
          data = json.load(f)
          for character in data:
            character_obj = data[character]
            try:
              definitions = character_obj['definition'].split('/')
              pinyin = character_obj['pinyin'].split('/')
              hsk_level = character_obj['hsk_level']
              frequency = character_obj['frequency']
              BaseCharacter(definitions=definitions, character=character, pinyin=pinyin, hsk_level=hsk_level, frequency=frequency)
            except KeyError as e:
              print(character, e)
