# model training
import pandas as pd
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.feature_extraction.text import TfidfVectorizer

import pickle

# data cleaning
from bs4 import BeautifulSoup
from nltk import tag
import json
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize


# url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
# names = ['preg', 'plas', 'pres', 'skin', 'test', 'mass', 'pedi', 'age', 'class']
# dataframe = pandas.read_csv(url, names=names)
# array = dataframe.values
# X = array[:,0:8]
# Y = array[:,8]
# test_size = 0.33
# seed = 7
# X_train, X_test, Y_train, Y_test = model_selection.train_test_split(X, Y, test_size=test_size, random_state=seed)
# # Fit the model on training set
# model = LogisticRegression()
# model.fit(X_train, Y_train)
# # save the model to disk
# filename = 'finalized_model.sav'
# pickle.dump(model, open(filename, 'wb'))
 
# some time later...
 
# load the model from disk
# loaded_model = pickle.load(open(filename, 'rb'))
# result = loaded_model.score(X_test, Y_test)
# print(result)


# nltk.download("stopwords")
# nltk.download('averaged_perceptron_tagger')
# nltk.download('punkt')
# nltk.download('wordnet')

def process_text(textArray):
  with open('resources/contractions.json', 'r') as f:
    contractions = json.load(f)
  contractions_keys = contractions.keys()
  replace_re_by_space = re.compile('[/(){}\[\]\|@,;]')
  delete_re_symbols = re.compile('[^0-9a-z #+_]')
  stop_words = set(stopwords.words('english'))

  def strip_html(text):
    soup = BeautifulSoup(text, features='lxml')
    return soup.get_text()

  def lowercase(text):
    return text.lower()

  def expand_contractions(text):
    return list(map(lambda word: contractions[word] if word in contractions_keys else word, text))

  def remove_symbols_punctuation(text):
    text = re.sub(delete_re_symbols.pattern, '', text)
    text = re.sub(replace_re_by_space.pattern, ' ', text)
    return text

  def remove_stop_words(text):
    filtered_sentence = [w for w in text if not w in stop_words]
    return filtered_sentence

  def text_lemmatization(text):
    wordnet_lemmatizer = WordNetLemmatizer()
    text = list(map(lambda word: wordnet_lemmatizer.lemmatize(word), text))
    return text

  return textArray.apply(lambda text: ' '.join(text_lemmatization(remove_stop_words(expand_contractions(word_tokenize(remove_symbols_punctuation(lowercase(strip_html(text)))))))))

# gets/cleans data, trains model, pickles model
def initModel():
  data = pd.read_csv('resources/Reviews.csv')
  print("Number of positive and negative reviews", '\n', data["sentiment"].value_counts())
  test_data = data.copy(deep=True)
  # test_data = data.head(20)
  test_data = test_data.assign(review = process_text(test_data["review"]))
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

initModel()



