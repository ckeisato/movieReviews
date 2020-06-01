
var url = "https://us-central1-poetic-avenue-237204.cloudfunctions.net/movieReviewSentiment/";

// url = 'http://localhost:5000';

function init() {
  console.log('herro');

  function getResults() {
    let formData = new FormData();
    formData.append('text', 'bad not good I hated it worst ever no good');

    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: JSON.stringify(formData)
    })
    .then(function(response) {
        // if (response.status !== 200) {
        //   console.log('Looks like there was a problem. Status Code: ' +
        //   response.status);
        //   return;
        // }
        // Examine the text in the response
      console.log("request done???", response);

      response.text().then(function(text) {
        if (text) {
          console.log("this text was returned back...", text);
        }
      });
    })
    .catch(function(err) {
      console.log('Fetch Error :-S', err);
    });
  }

  document.getElementById("analyze-text").onclick = getResults;
}

init();
