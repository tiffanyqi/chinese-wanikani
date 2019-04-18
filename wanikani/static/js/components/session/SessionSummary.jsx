import React from 'react';

import {getResponse} from '../../util';


export class SessionSummary extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      charactersCorrect: [],
      charactersIncorrect: [],
      user: null,
    }
    this._isMounted = false;
  }

  componentDidMount() {
    this._isMounted = true;
    this.fetchCorrectCharacters();
    this.fetchIncorrectCharacters();
    this.fetchUser();
  }

  componentWillUnmount() {
    this._isMounted = false;
  }

  render() {
    let {charactersCorrect, charactersIncorrect, user} = this.state;
    let sessionSummary = [];
    if (user) {
      if (user.last_session === 0) {
        sessionSummary = [
          <div key="session-first">Your session summary will appear here!</div>
        ];
      } else {
        const incorrectCharacters = charactersIncorrect.map(char => {
          return <div key={char.character}>{char.character}</div>;
        });
        const correctCharacters = charactersCorrect.map(char => {
          return <div key={char.character}>{char.character}</div>;
        });
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
    if (this._isMounted) {
      this.setState({charactersCorrect});
    }
  }

  async fetchIncorrectCharacters() {
    const charactersIncorrect = await getResponse(`/session/characters/incorrect/`);
    if (this._isMounted) {
      this.setState({charactersIncorrect});
    }
  }

  async fetchUser() {
    const user = await getResponse(`/user/`);
    if (this._isMounted) {
      this.setState({user});
    }
  }
}
