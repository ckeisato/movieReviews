# data cleaning
from bs4 import BeautifulSoup
from nltk import tag
import json
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import dill

# nltk.download("stopwords")
# nltk.download('averaged_perceptron_tagger')
# nltk.download('punkt')
# nltk.download('wordnet')

class Process_Text():
  contractions_file_path = 'resources/contractions.json'

  def __init__(self):
    with open('resources/contractions.json', 'r') as f:
      self.contractions = json.load(f)
    
    self.contractions_keys = self.contractions.keys()
    self.replace_re_by_space = re.compile('[/(){}\[\]\|@,;]')
    self.delete_re_symbols = re.compile('[^0-9a-z #+_]')
    self.stop_words = set(stopwords.words('english'))

  def strip_html(self, text):
    soup = BeautifulSoup(text, features='lxml')
    return soup.get_text()

  def lowercase(self, text):
    return text.lower()

  def expand_contractions(self, text):
    text = text.split()
    return ' '.join(list(map(lambda word: self.contractions[word] if word in self.contractions_keys else word, text)))

  def remove_symbols_punctuation(self, text):
    text = re.sub(self.delete_re_symbols.pattern, '', text)
    text = re.sub(self.replace_re_by_space.pattern, ' ', text)
    return text

  def remove_stop_words(self, text):
    text = text.split()
    filtered_sentence = [w for w in text if not w in self.stop_words]
    return filtered_sentence

  def text_lemmatization(self, text):
    wordnet_lemmatizer = WordNetLemmatizer()
    text = list(map(lambda word: wordnet_lemmatizer.lemmatize(word), text))
    return text

  def process_text(self, text):
    text = self.strip_html(text)
    text = self.expand_contractions(text)
    text = self.lowercase(text)
    text = self.remove_symbols_punctuation(text)
    text = self.remove_stop_words(text)
    text = self.text_lemmatization(text)
    return ' '.join(text)

  def process_text_array(self, textArray):
    return textArray.apply(lambda text: self.process_text(text))

dill.dump(Process_Text, open('serialized/process_text.sav', 'wb'))
