
var url = "http://us-central1-poetic-avenue-237204.cloudfunctions.net/movieReviewSentiment/";

// url = 'http://localhost:5000';

function init() {
  var cta = document.getElementById("analyze-cta");
  var input = document.getElementById("input");
  var demo = document.getElementById("demo");
  var reset = document.getElementById("reset-cta");
  var resultsPositive = document.getElementsByClassName("result-positive");
  var resultsNegative = document.getElementsByClassName("result-negative");
  
  function getResults() {
    demo.classList.add("loading");
    input.disabled = true;
    cta.disabled = true;
    reset.disabled = true;

    console.log("making the request!!!");

    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        text: input.value
      })
    })
    .then(function(response) {
      response.text().then(function(text) {
        console.log("Done with the request!!!!", text);
        if (text) {
          demo.classList.add("done");
          demo.classList.remove("loading");
          
          var results = JSON.parse(text);

          console.log("results", results);
          console.log("results.negative", results.negative);


          var positive = Math.round(parseFloat(results.positive) * 10000)/100;
          var negative = Math.round(parseFloat(results.negative) * 10000)/100;

          for (var i = 0; i < 2; i++) {
            resultsPositive[i].innerText = positive + '%';
            resultsNegative[i].innerText = negative + '%';
          }

          input.disabled = false;
          cta.disabled = false;
          reset.disabled = false;
        }
      });
    })
    .catch(function(err) {
      console.log('Fetch Error', err);
    });
  }

  function resetFields() {
    input.value = '';
    demo.classList.remove('done');
  }

  cta.onclick = getResults;
  reset.onclick = resetFields;
}

init();
