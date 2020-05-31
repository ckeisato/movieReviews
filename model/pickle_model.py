# model training
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
from process_text import process_text_array

# gets/cleans data, trains model, pickles model
def initModel():
  data = pd.read_csv('resources/Reviews.csv')
  print("Number of positive and negative reviews", '\n', data["sentiment"].value_counts())
  test_data = data.copy(deep=True)
  # test_data = data.head(20)
  test_data = test_data.assign(review = process_text_array(test_data["review"]))
  print("done cleaning data", test_data.head())

  # split data
  x_train, x_test, y_train, y_test = train_test_split(
    test_data["review"],
    test_data["sentiment"],
    test_size=0.3,
    random_state=42
  )

  print('done splitting data')

  # transform data
  vectorizer = TfidfVectorizer(max_df=0.9, min_df=0.0005, ngram_range=(1,2)).fit(x_train)

  print('done fitting vectorizer')

  x_train = vectorizer.transform(x_train)
  x_test = vectorizer.transform(x_test)

  print('done transforming text')

  # train model
  model = LogisticRegression(solver='lbfgs')
  model.fit(x_train, y_train)

  print('done fitting model, will start scoring')

  score = model.score(x_test, y_test)

  print('model score', score)

  pickle.dump(model, open('trained_model.sav', 'wb'))
  pickle.dump(vectorizer, open('trained_vectorizer.sav', 'wb'))

initModel()
