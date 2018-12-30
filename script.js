let character;
let type;

$(document).ready(function() {
  const url = 'http://ccdb.hemiola.com/characters/?filter=gb&fields=kDefinition,kMandarin,string';
  $.getJSON(url, function(data) {
    character = getRandomCharacter(data);
    type = getType();
  });

});

function getRandomCharacter(data) {
  const max = data.length;
  const randomNumber = getRandomNumber(max);
  const character = data[randomNumber];
  $('#character').text(function() {
    return character.string;
  });
}

function getType() {
  const randomNumber = getRandomNumber(2);
  const type = randomNumber === 0 ? 'definition' : 'pinyin';
  $('#type').text(function() {
    return `${type}:`;
  });
}

function validate() {
  const {character, type} = window;
  const userInput = $('#userInput').val();
  const key = type === 'definition' ? 'kDefinition' : 'kMandarin';
  const results = userInput === character[type] ? `you're right!` : `you're not right`;
  $('#results').text(function() {
    return results;
  });
  return false;
}

function getRandomNumber(max) {
  return Math.floor(Math.random() * max);
}
