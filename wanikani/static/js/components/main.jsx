import React from 'react';
import {Route, Switch} from 'react-router-dom';


export function Main() {
    return (
        <main>
            <Switch>
                <Route exact path='/home' component={Home}/>
                <Route path='/roster' component={Roster}/>
                <Route path='/schedule' component={Schedule}/>
            </Switch>
        </main>
    );
}

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

function Schedule() {
    return (
      <div>
        <ul>
          <li>6/5 @ Evergreens</li>
          <li>6/8 vs Kickers</li>
          <li>6/14 @ United</li>
        </ul>
      </div>
    );
  }
  
  function Home() {
    return (
      <div>
        <h1>Welcome to the Tornadoes Website!</h1>
      </div>
    );
  }

  function FullRoster() {
      return (
          <div>
              <h1>Full Roster</h1>
          </div>
      )
  }
