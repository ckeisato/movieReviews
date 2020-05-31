import pandas
from sklearn.model_selection import GridSearchCV, train_test_split
import pickle
import pandas as pd
import dill
import json
# from process_text import Process_Text

# for process text
from bs4 import BeautifulSoup
from nltk import tag
import json
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import dill

data = pd.read_csv('resources/Reviews.csv')

test_data = data.copy(deep=True)
# test_data = data.head(20)

# # split data
x_train, x_test, y_train, y_test = train_test_split(
  test_data["review"],
  test_data["sentiment"],
  test_size=0.001,
  random_state=42
)

# print('done splitting data')

# x_test = process_text_array(x_test)
loaded_process_text = dill.load(open('serialized/process_text.sav', 'rb'))

# process_text = loaded_process_text()

print(loaded_process_text("<p>I'm testing this text processer dogs!!"))
# print(process_text.process_text_array(x_test))

# print('done processing text')
# # load the model from disk
# loaded_vectorizer = pickle.load(open('trained_vectorizer.sav', 'rb'))
# # x_test = loaded_vectorizer.transform(x_test) 
# # print('done vectorizing', x_test)

# loaded_model = pickle.load(open('trained_model.sav', 'rb'))
# result = loaded_model.score(x_test, y_test)


# result = loaded_model.predict_proba(loaded_vectorizer.transform([process_text.process_text('this movie was really great I loved it very positive would watch again')]))
# print(result)

