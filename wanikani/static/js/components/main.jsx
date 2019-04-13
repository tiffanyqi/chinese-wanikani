import React from 'react';
import {Link, Route, Switch} from 'react-router-dom';

import {getData} from '../util.js';


export function Main() {
  return (
    <main>
      <Switch>
        <Route exact path='/index' component={Index}/>
        <Route path='/roster' component={Roster}/>
        <Route path='/characters' component={Characters}/>
      </Switch>
    </main>
  );
}

function Index() {
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

// TODO: remove this
function Roster() {
  return (
    <div>
      <h2>This is a roster page!</h2>
      <Switch>
        <Route exact path='/roster' component={FullRoster}/>
        <Route path='/roster/:number' component={Player}/>
      </Switch>
    </div>
  );
}

// TODO: remove this
function Player(props) {
  const player = {
    'name': 'hi',
    'number': props.match.params.number,
    'position': 'player',
  };
  if (!player) {
    return <div>Sorry, but the player was not found</div>
  }
  return (
    <div>
      <h1>{player.name} (#{player.number})</h1>
      <h2>{player.position}</h2>
    </div>
  );
}

class Characters extends React.Component {
  constructor() {
    super();
    this.state = {
      characters: [],
    }
  }

  async setCharacters() {
    const response = await getData('GET', '/characters/');
    const json = await response.json();
    this.setState({characters: json});
  }

  render() {
    this.setCharacters();
    const characterList = this.state.characters.map(char => {
      return (
        <li key={char.character}>
            {char.character}
        </li>
      );
    });

    return (
      <div>
        <h1>Characters</h1>
        <ul>{characterList}</ul>
      </div>
    )
  }
} 


  function FullRoster() {
      return (
          <div>
              <h1>Full Roster</h1>
          </div>
      )
  }
