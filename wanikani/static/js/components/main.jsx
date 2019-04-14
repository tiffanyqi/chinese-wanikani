import React from 'react';
import {Switch, Route} from 'react-router-dom';

import {Character} from './Character';
import {CharacterList} from './CharacterList';
import {Index} from './Index';


export class Main extends React.Component {
  render() {
    return (
      <main>
        <Switch>
          <Route 
            exact path='/'
            render={(props) => <Index {...props} user={this.props.user} />}
          />
          <Route path='/characters' component={Characters}/>
        </Switch>
      </main>
    );
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
