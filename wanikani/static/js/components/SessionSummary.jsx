import React from 'react';
import {Link} from 'react-router-dom';

import {getResponse} from '../util.js';


export class SessionSummary extends React.Component {
  constructor() {
    super();
    this.state = {
      charactersCorrect: [],
      charactersIncorrect: [],
    }
  }

  componentDidMount() {
    this.fetchCorrectCharacters();
    this.fetchIncorrectCharacters();
  }

  render() {
    let {correctCharacters, incorrectCharacters} = this.state;
    const {user} = this.props;
    let sessionSummary = [];
    if (!user || user.last_session === 0) {
      sessionSummary = [
        <div key="session-first">Your session summary will appear here!</div>
      ];
    } else {
      incorrectCharacters.map(char => {
        <div key={char.character}>{char.character.character}</div>
      });
      correctCharacters.map(char => {
        <div key={char.character}>{char.character.character}</div>
      })
      sessionSummary = [
        <div key="characters-incorrect">
          <h2>Incorrect</h2>
          <div>{incorrectCharacters}</div>
        </div>,
        <div key="characters-correct">
          <h2>Correct</h2>
          <div>{correctCharacters}</div>
        </div>
      ];
    }
    return (
      <div>
        <h1>Summary</h1>
        <div>You're done, you don't have any more characters to review!</div>
        <div>{sessionSummary}</div>
      </div>
    );
  }

  async fetchCorrectCharacters() {
    const charactersCorrect = await getResponse(`/session/characters/correct/`);
    this.setState({charactersCorrect});
  }

  async fetchIncorrectCharacters() {
    const charactersIncorrect = await getResponse(`/session/characters/incorrect/`);
    this.setState({charactersIncorrect});
  }
}
