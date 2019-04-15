import React from 'react';
import {Link} from 'react-router-dom';


export class Header extends React.Component {
  render() {
    const headerList = [
      <li key="header-index"><Link to="/">Dashboard</Link></li>,
      <li key="header-learn"><Link to="/session/learn">Learn</Link></li>,
      <li key="header-review"><Link to="/session/review">Review</Link></li>,
      <li key="header-characters"><Link to="/characters">Characters</Link></li>,
    ];
    if (this.props.user) {
      headerList.push(<li key="header-logout"><Link to="/logout">Logout</Link></li>);
    }

    return (
      <header>
        <nav>
          <ul>{headerList}</ul>
        </nav>
      </header>
    );
  }
}
