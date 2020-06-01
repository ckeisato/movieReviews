# data cleaning
from bs4 import BeautifulSoup
from nltk import tag
import json
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# nltk.download("stopwords")
# nltk.download('averaged_perceptron_tagger')
# nltk.download('punkt')
# nltk.download('wordnet')

with open('../model/resources/contractions.json', 'r') as f:
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

def process_text(text):
  return ' '.join(text_lemmatization(remove_stop_words(expand_contractions(word_tokenize(remove_symbols_punctuation(lowercase(strip_html(text))))))))

def process_text_array(textArray):
  return textArray.apply(lambda text: ' '.join(text_lemmatization(remove_stop_words(expand_contractions(word_tokenize(remove_symbols_punctuation(lowercase(strip_html(text)))))))))

