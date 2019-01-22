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

export function getRandomNumber(max) {
  return Math.floor(Math.random() * max);
}
