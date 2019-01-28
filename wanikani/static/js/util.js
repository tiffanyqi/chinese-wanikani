export function getData(method, url, data={}) {
  return fetch(url, {
    headers: {
      'Accept': 'application/json',
      'X-Requested-With': 'XMLHttpRequest'
    },
    method,
    credentials: 'include',
  });
}

export function postData(method, url, data={}) {
  return fetch(url, {
    body: data,
    headers: {
      'Accept': 'application/json',
      'X-Requested-With': 'XMLHttpRequest',
    },
    method,
    credentials: 'include',
  });
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

export function getRandomNumber(max) {
  return Math.floor(Math.random() * max);
}
