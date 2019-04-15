import React from 'react';

import {CSRFToken} from '../../csrftoken';
import {SESSION_STATE} from '../../session/constants';
import {
  getKey,
  getRandomCharacter,
  isUserCorrect,
  isWordComplete,
} from '../../session/helpers';
import {executeRequest, generateRandomNumbers, getCookie, getResponse} from '../../util';


export class Learn extends React.Component {
  constructor() {
    super();
    this.state = {
      anser: null,
      characterDisplayed: null,
      characterOrder: [],
      characterOrderNumber: null,
      characters: [],
      incrementSession: false, // from props?
      inputValue: ``,
      session: {},
      sessionNumber: null,
      showAnswer: false,
      sessionState: SESSION_STATE.received, // received, answering, answered, ready to move on
      typeSelected: null,
    }
    
    this.handleAnswerSubmitted = this.handleAnswerSubmitted.bind(this);
    this.handleDisplayAnswer = this.handleDisplayAnswer.bind(this);
    this.handleInputChange = this.handleInputChange.bind(this);
    this.handleInputKeyPress = this.handleInputKeyPress.bind(this);
    this.handleLoadRandomCharacter = this.handleLoadRandomCharacter.bind(this);
    this.handleSessionState = this.handleSessionState.bind(this);
  }

  componentDidMount() {
    this.fetchCharacters();
    if (this.state.incrementSession) {
      this.setState({
        sessionNumber: this.props.user.last_session + 1,
      });
    }

    document.addEventListener('keyup', this.handleSessionState);
  }

  render() {
    const {answer, characterDisplayed, inputValue, showAnswer, typeSelected} = this.state;
    if (characterDisplayed) {
      return (
        <div className="container">
          <div className="character-display">
            <div>{characterDisplayed.character}</div>
            <div>{typeSelected}</div>
          </div>
          <form onSubmit={this.handleAnswerSubmitted}>
            <CSRFToken />
            <input
              autoComplete="off"
              onChange={this.handleInputChange}
              id="session-character-input"
              onKeyPress={this.handleInputKeyPress}
              type="text"
              value={inputValue}
            />
            <input
              className={this.answerSubmitted() ? "disabled" : null}
              onClick={this.handleAnswerSubmitted}
              readOnly="Submit"
              type="Submit"
            />
            <button
              className={this.answerSubmitted() ? null : "disabled"}
              onClick={this.handleDisplayAnswer}
            >I don't know</button>
            <button
              className={this.answerSubmitted() ? null : "disabled"}
              onClick={this.handleLoadRandomCharacter}
            >Get another character</button>
          </form>
          {this.answerSubmitted() &&
            <div key="character-results">{answer}</div>
          }
          {showAnswer &&
            <div key="character-answer">{characterDisplayed[getKey(typeSelected)]}</div>
          }
        </div>
      );
    } else {
      // TODO: better loading
      return (
        <div>Loading</div>
      )
    }
  }

  // EVENT HANDLERS

  handleAnswerSubmitted(ev) {
    ev.preventDefault();
    const {characterDisplayed, characterOrder, characterOrderNumber, session, sessionNumber, sessionState, typeSelected} = this.state;
    if ([SESSION_STATE.received, SESSION_STATE.readyToMoveOn].includes(sessionState)) {
      return false;
    }
    const userInput = document.getElementById('session-character-input').value;
    const isCorrect = isUserCorrect(userInput, typeSelected, characterDisplayed);
    const answer = isCorrect ? `you're right!` : `you're not right`;
    const characterString = characterDisplayed.character;
    session[characterString][typeSelected] = isCorrect;

    let state = {
      answer,
      session,
      sessionState: SESSION_STATE.answered,
    }

    if (!isCorrect) {
      session[characterString]['incorrect'] = true;
      characterOrder.push(characterOrderNumber);
      state = {
        ...state,
        characterOrder,
      }
    }
    const isComplete = isWordComplete(session[characterString]);
    const areBothCorrect = !!(isComplete && !session[characterString]['incorrect']);

    executeRequest(`POST`, `/session/characters/learn/update/`, {
      both_correct: areBothCorrect,
      character: characterString,
      is_complete: isComplete,
      is_correct: isCorrect,
      session_number: sessionNumber,
      type: getKey(typeSelected),
    });
    this.setState(state);
    return false;
  }
  
  handleDisplayAnswer(ev) {
    if (ev.currentTarget.className === 'disabled') {
      ev.stopPropagation();
    } else {
      const {characterDisplayed, typeSelected} = this.state;
      const key = getKey(typeSelected);
      this.setState({answer: characterDisplayed[key]});
    }
    return false;
  }

  handleInputChange(ev) {
    this.setState({inputValue: ev.target.value});
  }

  handleInputKeyPress(ev) {
    if (ev.currentTarget.value && ev.keyCode !== 13) { // enter
      this.setState({sessionState: SESSION_STATE.answering});
    }
  }

  handleLoadRandomCharacter(ev) {
    if (ev && ev.currentTarget.className === 'disabled') {
      ev.stopPropagation();
    } else {
      this.loadRandomCharacter();
    }
    return false;
  }

  handleSessionState(ev) {
    if (ev.keyCode === 13) { // enter
      switch(this.state.sessionState) {
        case SESSION_STATE.received:
          document.getElementById('session-character-input').focus();
          break;
        case SESSION_STATE.answering:
          this.handleAnswerSubmitted(ev);
          break;
        case SESSION_STATE.answered:
          this.setState({sessionState: SESSION_STATE.readyToMoveOn});
          document.getElementById('session-character-input').blur();
          break;
        case SESSION_STATE.readyToMoveOn:
          this.loadRandomCharacter();
          break;
      }
    }
  }


  // HELPERS

  answerSubmitted() {
    return [SESSION_STATE.answered, SESSION_STATE.readyToMoveOn].includes(this.state.sessionState);
  }
  
  loadRandomCharacter() {
    this.clearFields();
    const {characters, characterOrder, session} = this.state;
    let {character, number, type} = getRandomCharacter(characters, characterOrder);
    if (!session[character.character]) {
      session[character.character] = {'incorrect': false};
    }
    this.setState({
      characterDisplayed: character,
      characterOrderNumber: number,
      session,
      typeSelected: type,
    });
  }

  clearFields() {
    this.setState({
      answer: null,
      characterDisplayed: null,
      characterOrderNumber: null,
      inputValue: ``,
      sessionState: SESSION_STATE.received,
      showAnswer: false,
      typeSelected: null,
    });
  }

  async fetchCharacters() {
    const characters = await getResponse(`/session/characters/learn/`);
    this.setState({
      characters,
      characterOrder: generateRandomNumbers(characters.length),
    });
    if (characters.length) {
      this.loadRandomCharacter();
    }
  }
}
