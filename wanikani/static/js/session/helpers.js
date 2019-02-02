import {CHARACTER_FIELDS, TEST_OPTIONS} from './constants.js';
import {getRandomNumber} from '../util.js';

export function getRandomCharacter(data) {
  // TODO: ensure there are no duplicates but each number appears twice for P/D
  const max = data.length;
  const randomNumber = getRandomNumber(max);
  const character = data[randomNumber];
  return character;
}

export function getType() {
  const randomNumber = getRandomNumber(2);
  const type = randomNumber === 0 ? TEST_OPTIONS.definition : TEST_OPTIONS.pinyin;
  return type;
}

export function getKey(type) {
  return isDefinition(type) ? CHARACTER_FIELDS.definition : CHARACTER_FIELDS.pinyin;
}

function isDefinition(type) {
  return type === TEST_OPTIONS.definition;
}

export function isUserCorrect(userInput, type, character) {
  const key = getKey(type);
  const possibleCorrectAnswers = isDefinition(type) ? character[key].split(/[,;]\s+/) : character[key].split(' ');
  const listOfAnswers = JSON.parse(possibleCorrectAnswers);
  let result = false;
  if (listOfAnswers.includes(userInput)) {
    result = true;
  } else if (listOfAnswers.includes(userInput.toUpperCase())) {
    result = true;
  }
  return result;
}

export function isWordComplete(character_object) {
  return !!(character_object[TEST_OPTIONS.pinyin] && character_object[TEST_OPTIONS.definition]);
}
