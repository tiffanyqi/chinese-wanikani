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
    this.state = {
      characterDisplayed: null,
      characterOrder: [],
      characterOrderNumber: null,
      characters: [],
      incrementSession: false, // from props?
      results: null,
      session: {},
      sessionNumber: null,
      state: SESSION_STATE.received, // received, answering, answered
      typeSelected: null,
    }
  }

  componentDidMount() {
    console.log(this.props);
    document.addEventListener('keyup', this.directSessionMethod);
    // TODO: remove jquery
    $('#session-character-input').keypress(function(ev) {
      if (ev.currentTarget.value && ev.keyCode !== 13) {
        window.state = SESSION_STATE.answering;
      }
    });

    this.fetchCharacters();
    if (this.state.incrementSession) {
      this.setState({
        sessionNumber: this.props.user.last_session + 1,
      });
    }
  }

  render() {
    const {characterDisplayed, results, typeSelected} = this.state;
    if (characterDisplayed) {
      return (
        <div className="container">
          <div className="character-display">
            <div id="session-character-displayed">{characterDisplayed.character}</div>
            <div id="session-character-type">{typeSelected}</div>
          </div>
          <div className="character-interaction">
            <input type="text" id="session-character-input" autoComplete="off"/>
            <input
              className={this.answerNotSubmitted() ? null : "disabled"}
              id="session-character-submit"
              onClick={() => this.handleAnswerSubmitted()}
              type="button"
              value="Submit"
            />
            <button
              className={this.answerNotSubmitted() ? "disabled" : null}
              id="session-character-get-answer"
              onClick={() => this.displayAnswer()}
            >I don't know</button>
            <button
              id="session-character-get-new-character"
              className={this.answerNotSubmitted() ? "disabled" : null}
              onClick={()=> this.loadRandomCharacter()}
            >Get another character</button>
          </div>
          <div id="session-character-results">{results}</div>
          <div id="session-character-answer">{characterDisplayed.pinyin}</div>
        </div>
      );
    } else {
      return (
        <div>Loading</div>
      )
    }
  }

  answerNotSubmitted() {
    return this.state.state === SESSION_STATE.received;
  }

  loadRandomCharacter(ev) {
    if (ev && ev.currentTarget.className === 'disabled') {
      ev.stopPropagation();
    } else {
      this.clearFields();
      const {characters, characterOrder, session} = this.state;
      let {character, number, type} = getRandomCharacter(characters, characterOrder);
      if (!session[character]) {
        session[character] = {'incorrect': false};
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
    session[characterString][type] = isCorrect;
    this.setState({session});

    if (!isCorrect) {
      session[characterString]['incorrect'] = true;
      characterOrder.push(characterOrderNumber);
      this.setState({characterOrder});
    }
    const isComplete = isWordComplete(session[characterString]);
    const areBothCorrect = !!(isComplete && !session[characterString]['incorrect']);
  
    // TODO: remove jquery
    $.post(updateCharacterURL, {
      both_correct: areBothCorrect,
      character: characterString,
      is_complete: isComplete,
      is_correct: isCorrect,
      session_number: sessionNumber,
      type: getKey(typeDisplayed),
      'csrfmiddlewaretoken': getCookie('csrftoken'),
    });
    return false;
  }
  
  displayAnswer(ev) {
    if (ev.currentTarget.className === 'disabled') {
      ev.stopPropagation();
    } else {
      const {character, type} = window;
      const key = getKey(type);
      $('#session-character-answer').text(() => character[key]);
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

  clearFields() {
    this.setState({
      ...this.state,
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
}
