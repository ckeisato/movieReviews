from flask import Flask, escape, request, jsonify
import pickle
import os
from google.cloud import storage
import json

# for text processing
from nltk import tag
import re
import nltk
from nltk.stem import WordNetLemmatizer
import dill

nltk.download('wordnet')

BUCKET = os.environ['BUCKET']
VECTORIZER_FILENAME = os.environ['VECTORIZER_FILENAME']
MODEL_FILENAME = os.environ['MODEL_FILENAME']
PROCESS_TEXT_FILENAME = os.environ['PROCESS_TEXT_FILENAME']

def predict_text(request):
    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)

    try:
        text = request.form.get('text')
        if text:
            client = storage.Client()
            bucket = client.get_bucket(BUCKET)
        
            vectorizer_blob = bucket.get_blob(VECTORIZER_FILENAME)
            model_blob = bucket.get_blob(MODEL_FILENAME)
            processtext_blob = bucket.get_blob(PROCESS_TEXT_FILENAME)
        
            vectorizer = pickle.loads(vectorizer_blob.download_as_string())
            model = pickle.loads(model_blob.download_as_string())
            process_text = dill.loads(processtext_blob.download_as_string())
            
            text = process_text(text)
            vectorized_text = vectorizer.transform([text])
            result = model.predict_proba(vectorized_text)
            return ((jsonify({ 'negative': result[0][0], 'positive': result[0][1]})), 200, headers)
        else:
            return ('Please send some review text thnx', 200, headers)
    except Exception as e:
        return (str(e), 500, headers)

    return ('something else happened (._.)', 200, headers)

