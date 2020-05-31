import pandas
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, train_test_split
import pickle
import pandas as pd

from process_text import process_text

data = pd.read_csv('resources/Reviews.csv')

test_data = data.copy(deep=True)
# test_data = data.head(20)

# split data
x_train, x_test, y_train, y_test = train_test_split(
  test_data["review"],
  test_data["sentiment"],
  test_size=0.01,
  random_state=42
)

print('done splitting data')

x_test = process_text(x_test)

print('done processing text')
# load the model from disk
loaded_vectorizer = pickle.load(open('trained_vectorizer.sav', 'rb'))
x_test = loaded_vectorizer.transform(x_test) 
print('done vectorizing', x_test)

loaded_model = pickle.load(open('trained_model.sav', 'rb'))
result = loaded_model.score(x_test, y_test)
print(result)

