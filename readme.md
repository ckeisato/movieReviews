 ## Sentiment Analysis

This is a demonstration for a machine learning model that determines whether a phrase is positive or negative.

#### Information about the model and application

- The model built using sklearn's logistic regression module.  The source code for how the model was trained and constructed can be found https://github.com/ckeisato/movieReviews/tree/master/model.

- The model is trained on corpus of movie reviews, so it will probably perform better with text that has similar language to a review.  More information on the data that was used can be found HERE.

- The model is run on a Google Cloud function.

- The request can take up to 10 seconds to complete, so please be patient.

#### todo:
- set up command line deployment for google cloud function
- migrate from cloud function to app engine?