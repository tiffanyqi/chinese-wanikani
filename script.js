$(document).ready(function() {
  $.getJSON('http://ccdb.hemiola.com/characters/?filter=gb&fields=kDefinition,kMandarin,string', function(data) {
    getRandomCharacter(data);
  });

});

function getRandomCharacter(data) {
  const max = data.length;
  const randomNumber = Math.floor(Math.random() * (max));
  const character = data[randomNumber];
  $('#character').text(function() {
    return character.string;
  });
}
