import React from 'react';

import {SessionSummary} from './SessionSummary';

import {SESSION_STATE} from './constants';
import {
  getKey,
  getRandomCharacter,
  isUserCorrect,
  isWordComplete,
} from './helpers';
import {CSRFToken} from '../../csrftoken';
import {executeRequest, generateRandomNumbers, getResponse} from '../../util';


export class Learn extends React.Component {
  render() {
    return (
      <Session incrementSession={false} sessionType="learn" showSummary={false} user={this.props.user} />
    )
  }
}

export class Review extends React.Component {
  render() {
    return (
      <Session incrementSession={true} showSummary={true} sessionType="review" user={this.props.user} />
    )
  }
}

export class Session extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      answer: null,
      characterDisplayed: null,
      characterOrder: [],
      characterOrderNumber: null,
      characters: null, // TODO: fix fetch requests to turn this into an array
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

    document.addEventListener('keyup', this.handleSessionState);
  }

  render() {
    const {answer, characterDisplayed, characters, inputValue, showAnswer, typeSelected} = this.state;
    if (characters) {
      if (!characters.length) {
        return (
          <SessionSummary />
        );
      }
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
                id="session-character-input"
                onChange={this.handleInputChange}
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
      } else if (this.props.showSummary) {
        return (
          <SessionSummary />
        );
      } else {
        return (
          <div>Loading</div>
        );        
      }
    } else {
      // TODO: better loading
      return (
        <div>Loading</div>
      );
    }
  }

  // EVENT HANDLERS

  handleAnswerSubmitted(ev) {
    ev.preventDefault();
    const {characterDisplayed, characterOrder, characterOrderNumber, inputValue, session, sessionNumber, sessionState, typeSelected} = this.state;
    if ([SESSION_STATE.received, SESSION_STATE.readyToMoveOn].includes(sessionState)) {
      return false;
    }
    const isCorrect = isUserCorrect(inputValue, typeSelected, characterDisplayed);
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

    executeRequest(`POST`, `/session/characters/${this.props.sessionType}/update/`, {
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
    const {characterDisplayed, sessionState} = this.state;
    if (ev.keyCode === 13) { // enter
      switch(sessionState) {
        case SESSION_STATE.received:
          if (characterDisplayed) {
            document.getElementById('session-character-input').focus();
          }
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
          document.getElementById('session-character-input').focus();
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
    if (character) {
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
    const characters = await getResponse(`/session/characters/${this.props.sessionType}/`);
    // TODO: move this all out somewhere
    const {incrementSession, user} = this.props;
    console.log(user);
    let state = {
      characters,
      characterOrder: generateRandomNumbers(characters.length),
    };
    if (incrementSession) {
      state = {
        ...state,
        sessionNumber: user.last_session + 1,
      };
    }
    this.setState(state);
    if (characters.length) {
      this.loadRandomCharacter();
    }
  }
}
