import React from 'react';
import {Link} from 'react-router-dom';

import {getResponse} from '../util.js';


export class Index extends React.Component {
  render() {
    const {user} = this.props;
    if (user) {
      return (
        <Dashboard user={user}/>
      );
    } else {
      return (
        <div>
          <h1>Welcome!</h1>
          {/* TODO: convert this to react? */}
          <div className="container">
            <a href="/registration/signup/"><button type="button">Sign Up</button></a>
            <a href="/registration/login/"><button type="button">Login</button></a>
          </div>
        </div>
      );
    }
  }
}

export class Dashboard extends React.Component {
  constructor() {
    super();
    this.state = {
      charactersAtLevel: [],
      charactersToLearn: [],
      charactersToReview: [],
    }
  }

  componentDidMount() {
    this.fetchCharactersAtLevel();
    this.fetchCharactersToLearn();
    this.fetchCharactersToReview();
  }

  render() {
    const {charactersAtLevel, charactersToLearn, charactersToReview} = this.state;
    const {user} = this.props;
    const charactersAtLevelList = charactersAtLevel.map(char => {
      return (
        <div className="character-container">
          <div className="character">
            <Link to={`/characters/${char.character}`}>{char.character}</Link>
          </div>
        </div>
      );
    });
    return (
      <div>
        <h1>Welcome!</h1>
        <div>Level: {user.level}</div>
        <div>Learn: {charactersToLearn.length}</div>
        <div>Review: {charactersToReview.length}</div>
        <div>{charactersAtLevelList}</div>
      </div>
    );
  }

  async fetchCharactersToLearn() {
    const charactersToLearn = await getResponse(`/request_characters/learn/`);
    this.setState({charactersToLearn});
  }

  async fetchCharactersToReview() {
    const charactersToReview = await getResponse(`/request_characters/review/`);
    this.setState({charactersToReview});
  }

  async fetchCharactersAtLevel() {
    const charactersAtLevel = await getResponse(`/request_characters/level/`);
    this.setState({charactersAtLevel});
  }
}
