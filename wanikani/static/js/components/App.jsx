import React from 'react';

import {Header} from './Header';
import {Main} from './Main';

import {getResponse} from '../util.js';


export class App extends React.Component {
  constructor() {
    super();
    this.state = {
      user: null,
    }
  }

  componentDidMount() {
    this.fetchUser();
  }

  render() {
    const {user} = this.state;
    return (
      <div>
        <Header
          user={user}
        />
        <Main
          user={user}
        />
      </div>
    );
  }

  async fetchUser() {
    const user = await getResponse(`/user/`);
    this.setState({user});
  }
}
