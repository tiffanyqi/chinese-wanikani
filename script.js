$(document).ready(function() {
  $.getJSON('http://ccdb.hemiola.com/characters/?filter=gb&fields=kDefinition,kMandarin,string', function(data) {
    data.forEach(function(character) {
      var tblRow = "<tr>" + "<td>" + character.string + "</td>" +
      "<td>" + character.kDefinition + "</td>" + "<td>" + character.kMandarin + "</td>" + "</tr>"
      $(tblRow).appendTo("#characters tbody");
    });
  });
});
