import {getData} from '../util.js';
import {getKey, getRandomCharacter, getType, isUserCorrect} from './helpers.js';


$(document).ready(function() {
  // move get data function here
  // change random character so that it's more separated and doesn't include duplicates
  loadRandomCharacter();
  $('#session-character-submit').click(validate);
  $('#session-character-get-answer').click(displayAnswer);
  $('#session-character-get-new-character').click(loadRandomCharacter);
  window.session = {};
});

function loadRandomCharacter() {
  getData('GET', 'current_level_characters_list')
    .then(result => result.json())
    .then(result => {
      window.character = getRandomCharacter(result);
      $('#session-character-displayed').text(() => window.character.character);
      window.type = getType();
      $('#session-character-type').text(() => `${window.type}:`);
      clearFields();
    });
  return false;
}

function validate() {
  const {character, type} = window;
  const userInput = $('#session-character-input').val();
  const isCorrect = isUserCorrect(userInput, type, character);
  const results = isCorrect ? `you're right!` : `you're not right`;
  window.session[character][type] = isCorrect;
  const isComplete = window.session[character].values().length == 2;
  $('#session-character-results').text(() => results);
  postData('POST', 'post_updated_character', {
    character,
    isComplete,
    isCorrect,
    type,
  });
  return false;
}

function displayAnswer() {
  const {character, type} = window;
  const key = getKey(type);
  $('#session-character-answer').text(() => character[key]);
  return false;
}

function clearFields() {
  $('#session-character-answer').text(() => '');
  $('#session-character').text(() => '');
  $('#session-character-results').text(() => '');
  if (document.getElementById('session-character-input')) {
    document.getElementById('session-character-input').value = '';
  }
}
