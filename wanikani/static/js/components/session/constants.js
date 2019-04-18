export const TEST_OPTIONS = {
  definition: 'definition',
  pinyin: 'pinyin',
}
export const CHARACTER_FIELDS = {
  definition: 'definitions',
  pinyin: 'pinyin',
}
export const SESSION_STATE = {
  answering: 'answering', // in the middle of answering
  answered: 'answered', // finished answering, see result
  received: 'received', // just see the question, hasn't typed anything
  readyToMoveOn: 'ready to move on', // ready to see the next question
}
