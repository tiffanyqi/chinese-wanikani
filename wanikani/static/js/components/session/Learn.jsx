import React from 'react';

import {CSRFToken} from '../../csrftoken';
import {SESSION_STATE} from '../../session/constants';
import {
  getKey,
  getRandomCharacter,
  isWordComplete,
  isUserCorrect,
} from '../../session/helpers';
import {generateRandomNumbers, getCookie, getResponse, executeRequest} from '../../util';


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
      sessionState: SESSION_STATE.received, // received, answering, answered
      typeSelected: null,
    }
  }

  componentDidMount() {
    this.fetchCharacters();
    if (this.state.incrementSession) {
      this.setState({
        sessionNumber: this.props.user.last_session + 1,
      });
    }

    document.addEventListener('keyup', this.directSessionMethod);
  }

  render() {
    const {characterDisplayed, results, showAnswer, typeSelected} = this.state;
    let characterResults = [];
    if (this.answerSubmitted()) {
      characterResults = [
        ...characterResults,
        <div>{results}</div>,
      ];
    }
    if (showAnswer) {
      characterResults = [
        ...characterResults,
        <div>{characterDisplayed.pinyin}</div>
      ];
    }

    if (characterDisplayed) {
      return (
        <div className="container">
          <div className="character-display">
            <div>{characterDisplayed.character}</div>
            <div>{typeSelected}</div>
          </div>
          <form onSubmit={(ev) => this.handleAnswerSubmitted(ev)}>
            <CSRFToken />
            <input
              autoComplete="off"
              id="session-character-input"
              onKeyPress={(ev) => this.handleInputKeyPress(ev)}
              type="text"
            />
            <input
              className={this.answerSubmitted() ? "disabled" : null}
              readOnly="Submit"
              type="Submit"
            />
            <button
              className={this.answerSubmitted() ? null : "disabled"}
              onClick={(ev) => this.displayAnswer(ev)}
            >I don't know</button>
            <button
              className={this.answerSubmitted() ? null : "disabled"}
              onClick={()=> this.loadRandomCharacter()}
            >Get another character</button>
          </form>
          {characterResults}
        </div>
      );
    } else {
      return (
        <div>Loading</div>
      )
    }
  }

  answerSubmitted() {
    return this.state.sessionState === SESSION_STATE.answered;
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

  handleAnswerSubmitted(ev) {
    ev.preventDefault();
    const {characterDisplayed, characterOrder, characterOrderNumber, session, sessionNumber, sessionState, typeSelected} = this.state;
    if (sessionState === SESSION_STATE.received) {
      return false;
    }
    const userInput = document.getElementById('session-character-input').value;
    const isCorrect = isUserCorrect(userInput, typeSelected, characterDisplayed);
    const results = isCorrect ? `you're right!` : `you're not right`;
    // TODO: set state once
    this.setState({
      results,
      sessionState: SESSION_STATE.answered,
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


    executeRequest(`POST`, `/session/update_learned_character`, {
      both_correct: areBothCorrect,
      character: characterString,
      is_complete: isComplete,
      is_correct: isCorrect,
      session_number: sessionNumber,
      type: getKey(typeSelected),
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
      switch(this.state.sessionState) {
        case SESSION_STATE.received:
          document.getElementById('session-character-input').focus();
          break;
        case SESSION_STATE.answering:
          this.handleAnswerSubmitted(ev);
          break;
        case SESSION_STATE.answered:
          this.loadRandomCharacter();
          break;
      }
    }
  }

  handleInputKeyPress(ev) {
    if (ev.currentTarget.value && ev.keyCode !== 13) {
      this.setState({sessionState: SESSION_STATE.answering});
    }
  }

  clearFields() {
    this.setState({
      ...this.state,
      answer: null,
      character: null,
      characterOrderNumber: null,
      results: null,
      sessionState: SESSION_STATE.received,
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
}
