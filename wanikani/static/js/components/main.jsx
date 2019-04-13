import React from 'react';
import {Route, Switch} from 'react-router-dom';

import {Character} from './Character';
import {CharacterList} from './CharacterList';


export function Main() {
  return (
    <main>
      <Switch>
        <Route exact path='/index' component={Index}/>
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
