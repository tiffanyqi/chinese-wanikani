import React from 'react';
import {Link} from 'react-router-dom';

import {getData} from '../util.js';


export class Header extends React.Component {
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
    const headerList = [
      <li key="index"><Link to="/">Dashboard</Link></li>,
      <li key="learn"><Link to="/learn">Learn</Link></li>,
      <li key="review"><Link to="/review">Review</Link></li>,
      <li key="characters"><Link to="/characters">Characters</Link></li>,
    ];
    if (this.state.user) {
      headerList.push(<li key="logout"><Link to="/logout">Logout</Link></li>);
    }

    return (
      <header>
        <nav>
          <ul>{headerList}</ul>
        </nav>
      </header>
    );
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
}
