import React from 'react';
import {Switch, Route} from 'react-router-dom';

import {Character} from './Character';
import {CharacterList} from './CharacterList';
import {Index} from './Index';
import {Session} from './Session';


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
            render={(props) => <Session {...props} incrementSession={false} sessionType="learn" user={user} />}
          />
          <Route
            path='/session/review'
            render={(props) => <Session {...props} incrementSession={true} sessionType="review" user={user} />}
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
