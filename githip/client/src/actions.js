export function fetchRepos(orgName) {
  return fetch(`/api/organization/${orgName}/repos`, {
    accept: "application/json"
  })
  .then(checkStatus)
  .then(parseJSON);
}


export function fetchRepoStats(orgName, repo) {
  return fetch(`/api/organization/${orgName}/repos/${repo}`, {
    accept: "application/json"
  })
  .then(checkStatus)
  .then(parseJSON);
}


function checkStatus(response) {
  if (response.status >= 200 && response.status < 300) {
    return response;
  }
  const error = new Error(`HTTP Error ${response.statusText}`);
  error.status = response.statusText;
  error.response = response;
  console.log(error); // eslint-disable-line no-console
  throw error;
}

function parseJSON(response) {
  return response.json();
}
