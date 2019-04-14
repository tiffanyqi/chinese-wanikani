import React from 'react';

import {SESSION_STATE} from '../../session/constants';
import {
  getKey,
  getRandomCharacter,
  isWordComplete,
  isUserCorrect,
} from '../../session/helpers';
import {generateRandomNumbers, getCookie, getResponse} from '../../util';


export class Learn extends React.Component {
  constructor() {
    super();
    this.directSessionMethod = this.directSessionMethod.bind(this),
    this.handleInputKeyPress = this.handleInputKeyPress.bind(this),
    this.state = {
      answer: null,
      characterDisplayed: null,
      characterOrder: [],
      characterOrderNumber: null,
      characters: [],
      incrementSession: false, // from props?
      results: null,
      session: {},
      sessionNumber: null,
      showAnswer: false,
      state: SESSION_STATE.received, // received, answering, answered
      typeSelected: null,
    }
  }

  componentDidMount() {
    this.fetchCharacters();
    // TODO: use prop instead of fetch
    this.fetchUser();

    document.addEventListener('keyup', this.directSessionMethod);
  }

  render() {
    const {characterDisplayed, results, showAnswer, state, typeSelected} = this.state;
    let characterResults = [];
    if (state === SESSION_STATE.answered) {
      characterResults = [
        ...characterResults,
        <div id="session-character-results">{results}</div>,
      ];
    }
    if (showAnswer) {
      characterResults = [
        ...characterResults,
        <div id="session-character-answer">{characterDisplayed.pinyin}</div>
      ];
    }

    if (characterDisplayed) {
      return (
        <div className="container">
          <div className="character-display">
            <div id="session-character-displayed">{characterDisplayed.character}</div>
            <div id="session-character-type">{typeSelected}</div>
          </div>
          <div className="character-interaction">
            <input
              autoComplete="off"
              id="session-character-input"
              onKeyPress={(ev) => this.handleInputKeyPress(ev)}
              type="text"
            />
            <input
              className={state !== SESSION_STATE.answered ? null : "disabled"}
              id="session-character-submit"
              onClick={() => this.handleAnswerSubmitted()}
              type="button"
              value="Submit"
            />
            <button
              className={state === SESSION_STATE.answered ? null : "disabled"}
              id="session-character-get-answer"
              onClick={() => this.displayAnswer()}
            >I don't know</button>
            <button
              id="session-character-get-new-character"
              className={state === SESSION_STATE.answered ? null : "disabled"}
              onClick={()=> this.loadRandomCharacter()}
            >Get another character</button>
          </div>
          {characterResults}
        </div>
      );
    } else {
      return (
        <div>Loading</div>
      )
    }
  }

  loadRandomCharacter(ev) {
    if (ev && ev.currentTarget.className === 'disabled') {
      ev.stopPropagation();
    } else {
      this.clearFields();
      const {characters, characterOrder, session} = this.state;
      let {character, number, type} = getRandomCharacter(characters, characterOrder);
      if (!session[character.character]) {
        session[character.character] = {'incorrect': false};
      }
      this.setState({
        ...this.state,
        characterDisplayed: character,
        characterOrderNumber: number,
        session,
        state: SESSION_STATE.received,
        typeSelected: type,
      })
    }
    return false;
  }

  handleAnswerSubmitted() {
    const {characterDisplayed, characterOrder, characterOrderNumber, session, state, typeSelected} = this.state;
    if (state === SESSION_STATE.received) {
      return false;
    }
    const userInput = document.getElementById('session-character-input').value;
    const isCorrect = isUserCorrect(userInput, typeSelected, characterDisplayed);
    const results = isCorrect ? `you're right!` : `you're not right`;
    // TODO: set state once
    this.setState({
      results,
      state: SESSION_STATE.answered,
    });
  
    const characterString = characterDisplayed.character;
    session[characterString][typeSelected] = isCorrect;
    this.setState({session});

    if (!isCorrect) {
      session[characterString]['incorrect'] = true;
      characterOrder.push(characterOrderNumber);
      this.setState({characterOrder});
    }
    const isComplete = isWordComplete(session[characterString]);
    const areBothCorrect = !!(isComplete && !session[characterString]['incorrect']);
  
    // TODO: remove jquery
    $.post(`/session/learn_character_list`, {
      both_correct: areBothCorrect,
      character: characterString,
      is_complete: isComplete,
      is_correct: isCorrect,
      session_number: sessionNumber,
      type: getKey(typeSelected),
      'csrfmiddlewaretoken': getCookie('csrftoken'),
    });
    return false;
  }
  
  displayAnswer(ev) {
    if (ev.currentTarget.className === 'disabled') {
      ev.stopPropagation();
    } else {
      const {character, typeSelected} = this.state;
      const key = getKey(typeSelected);
      this.setState({answer: character[key]});
    }
    return false;
  }

  directSessionMethod(ev) {
    ev.preventDefault();
    if (ev.keyCode === 13) { // enter
      switch(this.state.state) {
        case SESSION_STATE.received:
          document.getElementById('session-character-input').focus();
          break;
        case SESSION_STATE.answering:
          this.handleAnswerSubmitted();
          break;
        case SESSION_STATE.answered:
          this.loadRandomCharacter();
          break;
      }
    }
  }

  handleInputKeyPress(ev) {
    if (ev.currentTarget.value && ev.keyCode !== 13) {
      this.setState({state: SESSION_STATE.answering});
    }
  }

  clearFields() {
    this.setState({
      ...this.state,
      answer: null,
      character: null,
      characterOrderNumber: null,
      results: null,
      state: SESSION_STATE.received,
      typeSelected: null,
    })
    if (document.getElementById('session-character-input')) {
      document.getElementById('session-character-input').value = '';
    }
  }

  async fetchCharacters() {
    const characters = await getResponse(`/request_characters/learn/`);
    this.setState({
      characters,
      characterOrder: generateRandomNumbers(characters.length),
    });
    if (characters.length) {
      this.loadRandomCharacter();
    }
  }

  async fetchUser() {
    const user = await getResponse(`/user/`);
    if (this.state.incrementSession) {
      // TODO: get the actual session number
      this.setState({
        sessionNumber: user.last_session + 1,
      });
    }
  }
}
