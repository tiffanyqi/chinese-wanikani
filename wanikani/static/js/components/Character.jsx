import React from 'react';

import {getResponse} from '../util.js';


export class Character extends React.Component {
  constructor(props) {
    super(props);
    this.character = props.match.params.character,
    this.state = {
      characterObject: null,
    }
  }

  componentDidMount() {
    this.fetchCharacter();
  }

  render() {
    const character = this.state.characterObject;
    if (character) {
      return (
        <div className="container">
          <h1>{character.character}</h1>
          <ul>
            <li key="character-pinyin">Pinyin: {character.pinyin}</li>
            <li key="character-definition-">Definition: {character.definitions}</li>
            <li key="character-hsk-level">HSK Level: {character.hsk_level}</li>
            <li key="character-user-level">User Level: {character.user_level}</li>
          </ul>
        </div>
      );
    } else {
      return (
        <div>Character does not exist!</div>
      )
    }
  }

  async fetchCharacter() {
    const characterObject = await getResponse(`/request_characters/${this.character}/`);
    this.setState({characterObject});
  }
}
