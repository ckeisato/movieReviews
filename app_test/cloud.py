from flask import Flask, request, jsonify
from google.cloud import storage
import os
import pickle
import json

BUCKET = os.environ['BUCKET']
VECTORIZER_FILENAME = os.environ['VECTORIZER_FILENAME']
MODEL_FILENAME = os.environ['MODEL_FILENAME']

client = storage.Client()
bucket = client.get_bucket(BUCKET)

vectorizer_blob = bucket.get_blob(VECTORIZER_FILENAME)
model_blob = bucket.get_blob(MODEL_FILENAME)

vectorizer = pickle.loads(vectorizer_blob.download_as_string())
model = pickle.loads(model_blob.download_as_string())


def predict_text(request):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
    }

    try:
        request_json = request.get_json(silent=True)
        if request_json and 'text' in request_json:
            text = request_json['text']

            vectorized_text = vectorizer.transform([text])
            result = model.predict_proba(vectorized_text)
            return ((jsonify({ 'negative': result[0][0], 'positive': result[0][1]})), 200, headers)
        else:
            return ('Please send some review text thnx', 200, headers)
    except Exception as e:
        return (str(e), 500, headers)

    return ('something else happened (._.)', 200, headers)
