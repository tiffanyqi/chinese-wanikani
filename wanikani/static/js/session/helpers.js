import {CHARACTER_FIELDS, TEST_OPTIONS} from './constants.js';

export function getRandomCharacter(data, characterOrder) {
  /**
  * If the number is greater than the max, that is a definition, and the character in the
  * array is that number minus the max. If the number is less than the max, that
  * is the pinyin.
   */
  const max = data.length;
  const randomNumber = characterOrder.shift();
  const index = randomNumber > max ? randomNumber - max : randomNumber;
  const type = randomNumber > max ? TEST_OPTIONS.definition : TEST_OPTIONS.pinyin;
  const character = data[index];
  return {
    character,
    number: randomNumber,
    type,
  };
}

export function getKey(type) {
  return isDefinition(type) ? CHARACTER_FIELDS.definition : CHARACTER_FIELDS.pinyin;
}

function isDefinition(type) {
  return type === TEST_OPTIONS.definition;
}

export function isUserCorrect(userInput, type, character) {
  const key = getKey(type);
  const possibleCorrectAnswers = character[key].split(/[,;]\s+/);
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
