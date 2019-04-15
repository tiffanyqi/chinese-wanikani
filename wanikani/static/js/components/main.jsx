import React from 'react';
import {Switch, Route} from 'react-router-dom';

import {Character} from './Character';
import {CharacterList} from './CharacterList';
import {Index} from './Index';
import {Learn} from './session/Learn';


export class Main extends React.Component {
  render() {
    const {user} = this.props;
    return (
      <main>
        <Switch>
          <Route 
            exact path='/'
            render={(props) => <Index {...props} user={user} />}
          />
          <Route
            path='/session/learn'
            render={(props) => <Learn {...props} user={user} />}
          />
          <Route
            path='/characters'
            component={Characters}
          />
        </Switch>
      </main>
    );
  }
}

function Characters() {
  return (
    <div>
      <Switch>
        <Route
          exact path='/characters'
          component={CharacterList}
        />
        <Route
          path='/characters/:character'
          component={Character}
        />
      </Switch>
    </div>
  );
}
