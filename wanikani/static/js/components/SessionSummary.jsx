import React from 'react';
import {Link} from 'react-router-dom';

import {getResponse} from '../util.js';


export class SessionSummary extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      charactersCorrect: [],
      charactersIncorrect: [],
      user: null,
    }
  }

  componentDidMount() {
    this.fetchCorrectCharacters();
    this.fetchIncorrectCharacters();
    this.fetchUser();
  }

  render() {
    let {correctCharacters, incorrectCharacters, user} = this.state;
    let sessionSummary = [];
    if (user) {
      if (user.last_session === 0) {
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
    } else {
      return (
        <div>Loading</div>
      );
    }
  }

  async fetchCorrectCharacters() {
    const charactersCorrect = await getResponse(`/session/characters/correct/`);
    this.setState({charactersCorrect});
  }

  async fetchIncorrectCharacters() {
    const charactersIncorrect = await getResponse(`/session/characters/incorrect/`);
    this.setState({charactersIncorrect});
  }

  async fetchUser() {
    const user = await getResponse(`/user/`);
    this.setState({user});
  }
}
