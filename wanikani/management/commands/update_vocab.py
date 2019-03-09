from collections import OrderedDict
import json
import re

from django.core.management.base import BaseCommand

from wanikani.models import BaseCharacter

data = OrderedDict()

class Command(BaseCommand):

    def handle(self, *args, **options):
      self.extract_characters()
      self.dump_json()

    def extract_characters(self):
      with open('wanikani/static/data/sources/hsk-vocabulary.txt', 'r') as file:
        for line in file.read().split('\n'):
          split_line = line.split('\t')
          vocabulary = split_line[0]
          pinyin = split_line[2]
          definition = re.split(', •;', split_line[3])
          hsk_level = split_line[4]
          data[vocabulary] = {
            'hsk_level': hsk_level,
            'pinyin': pinyin,
            'definition': definition,
            'type': 'vocabulary',
            # 'level': self.apply_level(vocabulary),
          }
    
    def apply_level(self, vocabulary):
      # temp
      return 1

    def dump_json(self):
      with open('wanikani/static/data/vocabulary.json', 'w') as outfile:
        reverse_dict = OrderedDict(reversed(list(data.items())))
        json.dump(reverse_dict, outfile, ensure_ascii=False)
