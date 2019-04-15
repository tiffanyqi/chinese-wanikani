import React from 'react';
import {Link} from 'react-router-dom';

import {getResponse} from '../util.js';


export class CharacterList extends React.Component {
  constructor() {
    super();
    this.state = {
      characters: [],
    }
  }

  componentDidMount() {
    this.fetchCharacters();
  }

  render() {
    const characterList = this.state.characters.map(char => {
      return (
        <li key={char.character}>
          <Link to={`/characters/${char.character}`}>{char.character}</Link>
        </li>
      );
    });

    return (
      <div className="container">
        <h1>Characters</h1>
        <ul>{characterList}</ul>
      </div>
    )
  }

  async fetchCharacters() {
    const characters = await getResponse(`/session/characters/`);
    this.setState({characters});
  }
}
