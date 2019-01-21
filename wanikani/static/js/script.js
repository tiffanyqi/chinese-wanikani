/* User input functions */
$(document).ready(function() {
  loadRandomCharacter();
});

function loadRandomCharacter() {
  callData('GET', '/characters_list')
    .then(result => result.json())
    .then(result => {
      window.character = getRandomCharacter(result);
      $('#tested-character').text(function() {
        return window.character.character;
      });
      window.type = getType();
      $('#type').text(function() {
        return `${window.type}:`;
      });
      clearFields();
    });
  return false;
}

function validate() {
  const {character, type} = window;
  const userInput = $('#userInput').val();
  const results = isUserCorrect(userInput, type, character) ? `you're right!` : `you're not right`;
  $('#results').text(function() {
    return results;
  });
  return false;
}

function displayAnswer() {
  const {character, type} = window;
  const key = getKey(type);
  $('#answer').text(function() {
    return character[key];
  });
  return false;
}

function clearFields() {
  $('#answer').text(function() {
    return '';
  });
  $('#character').text(function() {
    return '';
  });
  $('#results').text(function() {
    return '';
  });
  if (document.getElementById('userInput')) {
    document.getElementById('userInput').value = '';
  }
}

/* Helper functions */

function getRandomNumber(max) {
  return Math.floor(Math.random() * max);
}

function getRandomCharacter(data) {
  const max = data.length;
  const randomNumber = getRandomNumber(max);
  const character = data[randomNumber];
  return character;
}

function getType() {
  const randomNumber = getRandomNumber(2);
  const type = randomNumber === 0 ? 'definition' : 'pinyin';
  return type;
}

function getKey(type) {
  return isDefinition(type) ? 'definitions' : 'pinyin';
}

function isDefinition(type) {
  return type === 'definition';
}

function isUserCorrect(userInput, type, character) {
  const key = getKey(type);
  const possibleCorrectAnswers = isDefinition(type) ? character[key].split(/[,;]\s+/) : character[key].split(' ');
  let result = false;
  if (possibleCorrectAnswers.includes(userInput)) {
    result = true;
  } else if (possibleCorrectAnswers.includes(userInput.toUpperCase())) {
    result = true;
  }
  return result;
}

/* AUTH */
function callData(method, url, data={}) {
  return fetch(url, {
    headers: {
      'Accept': 'application/json',
      'X-Requested-With': 'XMLHttpRequest'
    },
    method,
    credentials: 'include',
  });
}