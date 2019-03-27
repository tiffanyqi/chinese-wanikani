from collections import OrderedDict
import json
import re

from django.core.management.base import BaseCommand

data = OrderedDict()

class Command(BaseCommand):
    """
    Updates the character data file from various sources.
    """
    def handle(self, *args, **options):
      self.extract_hsk_level()
      self.extract_characters()
      self.dump_json()

    def extract_hsk_level(self):
      with open('wanikani/static/data/sources/hsk.txt', 'r') as file:
        for line in file:
          split_line = line.split(', ')
          level = int(split_line[0])
          characters = split_line[1]
          for character in characters.split(' '):
            data[character] = {'hsk_level': level}

    def extract_characters(self):
      with open('wanikani/static/data/sources/character-frequency.txt', 'r') as file:
        for line in file.read().split('\n'):
          split_line = line.split('\t')
          frequency_order = int(split_line[0])
          character = split_line[1]
          pinyin = split_line[4].split('/')
          definition = re.split(', |/', split_line[5])
          try:
            data[character].update({
              'frequency': frequency_order,
              'pinyin': pinyin,
              'definition': definition,
              'type': 'character',
            })
          except KeyError:
            print(character, ' does not exist in the data set')

    def dump_json(self):
      with open('wanikani/static/data/characters.json', 'w') as outfile:
        json.dump(data, outfile, ensure_ascii=False)
