Chinese version of Wanikani
==
Wanikani is a great way to learn kanji. According to the forums, there's no good app that does what Wanikani does for Chinese. So, here's my attempt at that.

- Based on the HSK, or the Chinese Proficiency Test, which covers 2663 characters and 5000 vocabulary words. This represents 97.97% of everyday written language according to the Hutong School.
- Individual character and frequency data from http://lingua.mtsu.edu/chinese-computing/statistics/char/list.php?Which=MO
- Radical data from https://www.yellowbridge.com/chinese/radicals.php
- HSK data from http://huamake.com/1to6Lists.htm
- Dictionary data from https://www.mdbg.net/chinese/dictionary?page=cedict
- Other character data from http://ccdb.hemiola.com/characters/?filter=gb&fields=kDefinition,kMandarin,string, which came from http://www.unicode.org/charts/unihan.html
- City and province data from https://en.wikipedia.org/wiki/List_of_cities_in_China_by_population_and_built-up_area
- Idioms from https://www.saporedicina.com/english/list-chengyu/ and https://www.chinasage.info/proverbstrive.htm

# Initializing the app
- Ensure you have python 3.7
- `brew install pipenv`, linked to python 3.7
- ensure you have postgresql installed, version 9.6
- `pipenv shell`, creates a virtual environment
- `pipenv install`, installs all packages within that virtual environment
- `pg_ctl -D /usr/local/var/postgres start` , run postgres
- initialize the database with the following:
```
psql postgres
CREATE DATABASE wanikani;
CREATE ROLE username WITH PASSWORD 'password';
```
- `python3 manage.py runserver`, runs the app! now go to localhost:8000 to ensure it works
- run `bash wanikani/management/commands/setup_db.sh` to populate characters and vocabulary in the database
- create a user! This will automatically create ProgressCharacters for you.

# Running the app
- `pipenv shell` creates the virtual environment for you with everything installed ideally
- create two windows or screens with one in the following:
- `npm run watch` runs webpack in watch mode, manually refresh the browser to view changes
- `python3 manage.py runserver`, runs the server, will show up as localhost:8000 (run this in the virtual environment)

# Schema:
- Each character has its own information based on the full JSON dictionary and various information from the user
- User class
- Session class - each review or lesson session

# TODOs:

## WEBAPP
- home page - characters of your level and your progress
- learning page
- review page - remember which characters are correct and which are wrong
- all characters page
  - display the number of characters learned and will be learned
  - display characters in order by level
- settings page
- make it look nice
- quiz so that users can skip to the appropriate level

## Learning system
- Apprentice/Guru/Master/Burned
- Timing for when to learn again: https://knowledge.wanikani.com/wanikani/srs-stages/

## V2
- incorporate sound to characters
- leveling streak?
- character breakdown
- explanation breakdown
