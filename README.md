Chinese version of Wanikani
==
Wanikani is a great way to learn kanji. According to the forums, there's no good app that does what Wanikani does for Chinese. So, here's my attempt at that.

- Based on the HSK, or the Chinese Proficiency Test, which covers 2663 characters and 5000 vocabulary words. This represents 97.97 % of everyday written language according to the Hutong School.
- Individual character and frequency data from http://lingua.mtsu.edu/chinese-computing/statistics/char/list.php?Which=MO
- HSK data from http://huamake.com/1to6Lists.htm
- Dictionary data from https://www.mdbg.net/chinese/dictionary?page=cedict
- Other character data from http://ccdb.hemiola.com/characters/?filter=gb&fields=kDefinition,kMandarin,string, which came from http://www.unicode.org/charts/unihan.html


Schema

User {
  name,
  email,
  level,
}
Character {
  string,
  user level,
  frequency,
  definitions,
  pronunciations,
  sound byte?,
  user,
  encountered,
  % correct pronunciation,
  % correct meaning,
  hsk level,
  level (apprentice, etc)
}

==
TODOs:

WEBAPP
- connect to django
- display the number of characters learned and will be learned
- display characters in order by level
- connect to sound?
- 

DB
- save characters in db
- remember which characters are correct and which are wrong
- add vocab

Learning system
- Leveling
- Apprentice/Guru/Master/Burned
- Timing for when to learn again
