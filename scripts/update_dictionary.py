import json

data = {}

# extracts HSK level
with open('data/hsk.txt', 'r') as file:
  for line in file:
    split_line = line.split(', ')
    level = split_line[0]
    characters = split_line[1]
    for character in characters.split(' '):
      data[character] = {'hsk_level': level}

# extracts character frequencies, pinyin, and definition
with open('data/character-frequency.txt', 'r') as file:
  for line in file:
    split_line = line.split('\t')
    frequency_order = split_line[0]
    character = split_line[1]
    pinyin = split_line[4]
    definition = split_line[5]
    try:
      data[character].update({
        'frequency': frequency_order,
        'pinyin': pinyin,
        'definition': definition,
      })
    except KeyError as e:
      print(character, ' does not exist in the data set')

with open('data/data.json', 'w') as outfile:  
  json.dump(data, outfile)
