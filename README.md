Chinese version of Wanikani
==
Wanikani is a great way to learn kanji. According to the forums, there's no good app that does what Wanikani does for Chinese. So, here's my attempt at that.

- Based on the HSK, or the Chinese Proficiency Test, which covers 2663 characters and 5000 vocabulary words. This represents 97.97% of everyday written language according to the Hutong School.
- Individual character and frequency data from http://lingua.mtsu.edu/chinese-computing/statistics/char/list.php?Which=MO
- HSK data from http://huamake.com/1to6Lists.htm
- Dictionary data from https://www.mdbg.net/chinese/dictionary?page=cedict
- Other character data from http://ccdb.hemiola.com/characters/?filter=gb&fields=kDefinition,kMandarin,string, which came from http://www.unicode.org/charts/unihan.html

# Schema:
- Each character has its own information based on the full JSON dictionary and various information from the user
- User class
- Session class - each review or lesson session

# Database population:
- Save characters in the database: `python3 manage.py populate_characters_in_db`
- Update levels for characters: `python3 manage.py update_levels`

# TODOs:

## WEBAPP
- home page - characters of your level and your progress
- learning page
- review page - remember which characters are correct and which are wrong
- all characters page
  - display the number of characters learned and will be learned
  - display characters in order by level
- individual character page
- settings page
- signup/login page
- make it look nice
- make an API call to the DB whenever user gets something wrong or right

## Learning system
- Apprentice/Guru/Master/Burned
- Timing for when to learn again: https://knowledge.wanikani.com/wanikani/srs-stages/

## V2
- incorporate sound to characters
- leveling streak?
- character breakdown
- explanation breakdown
- user input
- vocabulary from dictionary