import React from 'react';
import {Route, Link, Switch} from 'react-router-dom';

import {Character} from './Character';
import {CharacterList} from './CharacterList';

import {getData} from '../util.js';


export function Main() {
  return (
    <main>
      <Switch>
        <Route exact path='/' component={Index}/>
        <Route path='/characters' component={Characters}/>
      </Switch>
    </main>
  );
}

export class Index extends React.Component {
  constructor() {
    super();
    this.state = {
      charactersAtLevel: [],
      charactersToLearn: [],
      charactersToReview: [],
      user: null,
    }
  }

  componentDidMount() {
    this.fetchUser();
    this.fetchCharactersAtLevel();
    this.fetchCharactersToLearn();
    this.fetchCharactersToReview();
  }

  render() {
    const {charactersAtLevel, charactersToLearn, charactersToReview, user} = this.state;
    const charactersAtLevelList = charactersAtLevel.map(char => {
      return (
        <div className="character-container">
          <div className="character">
            <Link to={`/characters/${char.character}`}>{char.character}</Link>
          </div>
        </div>
      );
    });
    if (user) {
      return (
        <div>
          <h1>Welcome!</h1>
          <div>Level: {user.level}</div>
          <div>Learn: {charactersToLearn.length}</div>
          <div>Review: {charactersToReview.length}</div>
          <div>{charactersAtLevelList}</div>
        </div>
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

  async fetchUser() {
    try {
      const response = await getData('GET', '/user/');
      if (!response.ok) {
        throw Error(response.statusText);
      }
      const json = await response.json();
      this.setState({user: json });
    } catch (error) {
      console.log(error);
    }
  }

  async fetchCharactersToLearn() {
    try {
      const response = await getData('GET', '/request_characters/learn/');
      if (!response.ok) {
        throw Error(response.statusText);
      }
      const json = await response.json();
      this.setState({charactersToLearn: json });
    } catch (error) {
      console.log(error);
    }
  }

  async fetchCharactersToReview() {
    try {
      const response = await getData('GET', '/request_characters/review/');
      if (!response.ok) {
        throw Error(response.statusText);
      }
      const json = await response.json();
      this.setState({charactersToReview: json });
    } catch (error) {
      console.log(error);
    }
  }

  async fetchCharactersAtLevel() {
    try {
      const response = await getData('GET', '/request_characters/level/');
      if (!response.ok) {
        throw Error(response.statusText);
      }
      const json = await response.json();
      this.setState({charactersAtLevel: json });
    } catch (error) {
      console.log(error);
    }
  }
}

function Characters() {
  return (
    <div>
      <Switch>
        <Route exact path='/characters' component={CharacterList}/>
        <Route path='/characters/:character' component={Character}/>
      </Switch>
    </div>
  );
}
