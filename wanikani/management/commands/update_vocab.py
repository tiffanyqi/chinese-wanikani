from collections import OrderedDict
import json
import re

from django.core.management.base import BaseCommand

from wanikani.models import BaseCharacter

data = OrderedDict()

class Command(BaseCommand):
    """
    Updates the vocabulary data file from various sources. Also assigns the user level
    in the data file.
    """
    def handle(self, *args, **options):
      self.extract_characters()
      self.dump_json()

    def extract_characters(self):
      self.extract_hsk()
      self.extract_food()

    def extract_hsk(self):
      with open('wanikani/static/data/sources/hsk-vocabulary.txt', 'r') as file:
        for line in file.read().split('\n'):
          split_line = line.split('\t')
          vocabulary = split_line[0]
          if self.check_character_stored(vocabulary):
            pinyin = split_line[2]
            definition = re.split('; | • ', split_line[3])
            hsk_level = split_line[4]
            data[vocabulary] = self.get_data(pinyin, definition, vocabulary)
            data[vocabulary]['hsk_level'] = hsk_level


    def extract_food(self):
      with open('wanikani/static/data/sources/foods.txt', 'r') as file:
        for line in file.read().split('\n')[1:]:
          split_line = line.split('\t')
          chinese = split_line[3]
          if self.check_character_stored(chinese):
            definition = split_line[0]
            pinyin = split_line[5]
            data[chinese] = self.get_data(pinyin, definition, chinese)
          else:
            print(chinese, "not in database")


    def get_data(self, pinyin, definition, chinese):
      return {
        'pinyin': pinyin,
        'definition': definition,
        'type': 'vocabulary',
        'level': self.apply_level(chinese),
      }

    
    def check_character_stored(self, vocabulary):
      for character in vocabulary:
        try:
          BaseCharacter.objects.get(character=character)
        except BaseCharacter.DoesNotExist:
          return False
      return True

    def apply_level(self, vocabulary):
      max_level = 1
      for character in vocabulary:
        base_character = BaseCharacter.objects.get(character=character)
        max_level = max(max_level, base_character.user_level)
      return max_level

    def dump_json(self):
      with open('wanikani/static/data/vocabulary.json', 'w') as outfile:
        reverse_dict = OrderedDict(reversed(list(data.items())))
        json.dump(reverse_dict, outfile, ensure_ascii=False)
