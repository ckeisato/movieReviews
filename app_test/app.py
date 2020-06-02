from flask import Flask, escape, request, jsonify
import pickle
import pandas as pd
# from process_text import process_text

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def main():
  headers = {
    'Access-Control-Allow-Origin': '*'
  }

  request_json = request.get_json(silent=True)
  print(request_json)
  if request_json and 'name' in request_json:
    name = request_json['name']
    return (name, 200, headers)
  # loaded_vectorizer = pickle.load(open('../model/trained_vectorizer.sav', 'rb'))
  # loaded_model = pickle.load(open('../model/trained_model.sav', 'rb'))

  # # result = loaded_model.predict_proba(loaded_vectorizer.transform([process_text(text)]))
  # print(text)
  # text = loaded_vectorizer.transform([text])
  # result = loaded_model.predict_proba(text)

  # print(result)
  return ('did not work', 200, headers)


# env FLASK_APP=app.py flask run