Chinese version of Wanikani
==
Wanikani is a great way to learn kanji. According to the forums, there's no good app that does what Wanikani does for Chinese. So, here's my attempt at that.

- Individual character data from http://ccdb.hemiola.com/characters/?filter=gb&fields=kDefinition,kMandarin,string, which came from http://www.unicode.org/charts/unihan.html
- Used the GB2312 (6763 characters, which represents 99% of contemporary characters), which is the simplified version used in Mainland China
- Dictionary data from https://www.mdbg.net/chinese/dictionary?page=cedict
- Frequency data from http://lingua.mtsu.edu/chinese-computing/statistics/char/list.php?Which=MO
- HSK data from http://huamake.com/1to6Lists.htm

Schema

User
Character {
  string,
  level,
  frequency,
  definitions,
  pronunciations,
  sound byte?,
  user,
  % correct pronunciation,
  % correct meaning,
}

==
TODOs:

WEBAPP
- connect to django
- implement SRS
- implement level system
- display the number of characters learned and will be learned
- display characters in order by level
- connect to sound?

DB
- save characters in db
- remember which characters are correct and which are wrong
- add vocab
