export function executeRequest(method, url, body={}) {
  let data = {
    credentials: 'include',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken'),
    },
    method,
  };
  if (method === `POST`) {
    data = {
      ...data,
      body: JSON.stringify(body),
    }
  }
  return fetch(url, data);
}

export async function getResponse(url) {
  try {
    const response = await executeRequest('GET', url);
    if (!response.ok) {
      throw Error(response.statusText);
    }
    const json = await response.json();
    return json;
  } catch (error) {
    console.log(error);
  }
}

// Helper function to grab cookies, mostly for csrf
export function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) == (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

export function generateRandomNumbers(max) {
  /**
   * This function generates the order in which a user answers accordingly.
   * It generates a random list of numbers double the size of the length
   * of the number of characters to subdivide between pinyin and definition.
   */
  const numberArray = Array.apply(null, {length: max*2}).map(Number.call, Number);
  return shuffle(numberArray);
}

// https://stackoverflow.com/questions/2450954/how-to-randomize-shuffle-a-javascript-array
function shuffle(array) {
  var currentIndex = array.length, temporaryValue, randomIndex;

  // While there remain elements to shuffle...
  while (0 !== currentIndex) {

    // Pick a remaining element...
    randomIndex = Math.floor(Math.random() * currentIndex);
    currentIndex -= 1;

    // And swap it with the current element.
    temporaryValue = array[currentIndex];
    array[currentIndex] = array[randomIndex];
    array[randomIndex] = temporaryValue;
  }

  return array;
}
