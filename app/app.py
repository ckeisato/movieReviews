from flask import Flask, escape, request, jsonify
import pickle
import pandas as pd
from process_text import process_text

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def main():
  text = request.form.get('text')

  loaded_vectorizer = pickle.load(open('../model/trained_vectorizer.sav', 'rb'))
  loaded_model = pickle.load(open('../model/trained_model.sav', 'rb'))
  result = loaded_model.predict_proba(loaded_vectorizer.transform([process_text(text)]))
  print(result)
  return (jsonify({ 'negative': result[0][0], 'positive': result[0][1]}))
