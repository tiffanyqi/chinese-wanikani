import {CHARACTER_FIELDS, TEST_OPTIONS} from './constants.js';
import {getRandomNumber} from '../util.js';

export function getRandomCharacter(data) {
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
  return isDefinition(type) ? CHARACTER_FIELDS.definitions : CHARACTER_FIELDS.pinyin;
}

function isDefinition(type) {
  return type === TEST_OPTIONS.definition;
}

export function isUserCorrect(userInput, type, character) {
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
