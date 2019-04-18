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
    const characterList = [];
    Array.from(Array(60), (_,x) => x + 1).forEach(level => {
      const levelCharacters = this.getCharactersOfLevel(level);
      characterList.push(
        <div className={`character-level-container`} key={`level-list-${level}`}>
          <div className={`character-level`}>{level}</div>
          <div className={`character-level-characters`}>{levelCharacters}</div>
        </div>
      )
    });
    return (
      <div className="container">
        <h1>Characters</h1>
        <ul>{characterList}</ul>
      </div>
    )
  }

  getCharactersOfLevel(level) {
    const characterList = [];
    this.state.characters.filter(char => char.user_level === level).forEach(char => {
      characterList.push(
        <div key={char.character}>
          <Link to={`/characters/${char.character}`}>{char.character}</Link>
        </div>
      );
    });
    return characterList;
  }

  async fetchCharacters() {
    const characters = await getResponse(`/session/characters/`);
    this.setState({characters});
  }
}
