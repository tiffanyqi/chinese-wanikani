import json

data = {}

# extracts characters from GB2312 and saves their pinyin and definition
with open('data/character-to-definition.json', 'r') as file:
  for character in json.loads(file.read()):
    data[character['string']] = {
      'pinyin': character['kMandarin'],
      'definition': character['kDefinition'],
    }

# extracts character frequencies
with open('data/character-frequency.txt', 'r') as file:
  for line in file:
    split_line = line.split('\t')
    frequency_order = split_line[0]
    character = split_line[1]
    try:
      data[character].update({'frequency': frequency_order})
    except KeyError as e:
      print(character, ' does not exist in the frequency list')

# extracts HSK level
with open('data/hsk.txt', 'r') as file:
  for line in file:
    split_line = line.split(', ')
    level = split_line[0]
    characters = split_line[1]
    for character in characters.split(' '):
      try:
        data[character].update({'level': level})
      except KeyError as e:
        print(character, ' does not exist in the HSK list')

# saves data
with open('data/data.json', 'w') as outfile:  
    json.dump(data, outfile)
