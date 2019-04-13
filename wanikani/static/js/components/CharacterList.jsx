import React from 'react';
import {Link} from 'react-router-dom';

import {getData} from '../util.js';


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
    try {
      const response = await getData('GET', '/request_characters/');
      if (!response.ok) {
        throw Error(response.statusText);
      }
      const json = await response.json();
      this.setState({characters: json });
    } catch (error) {
      console.log(error);
    }
  }
}
