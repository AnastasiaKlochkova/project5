# Importing the required libraries
import requests
import os
import uuid
import json
from dotenv import load_dotenv
from flask import Flask, render_template, request

load_dotenv()
app = Flask(__name__)

# возвращает index
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def index_post():
    # читает форму
    original_text = request.form['text']
    target_language = request.form['language']

    # .env
    key = os.environ['KEY']
    endpoint = os.environ['ENDPOINT']
    location = os.environ['LOCATION']


    path = '/translate?api-version=3.0'

    # язык на который нужно перейти
    target_language_parameter = '&to=' + target_language

    # полная сборка URL
    constructed_url = endpoint + path + target_language_parameter

    # заголовок
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # что передаем на азуру
    body = [{'text': original_text}]


    translator_request = requests.post(
        constructed_url, headers=headers, json=body)

    # расшифровали json в обычный список
    translator_response = translator_request.json()

    # взяли необходимые данные (текст перевода)
    translated_text = translator_response[0]['translations'][0]['text']

    return render_template(
        'results.html',
        translated_text=translated_text,
        original_text=original_text,
        target_language=target_language
    )
