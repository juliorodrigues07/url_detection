from datamining.preprocessing import url_protocol
from datamining.preprocessing import count_digits
from datamining.preprocessing import count_dirs
from datamining.preprocessing import first_directory
from datamining.preprocessing import count_dots
from datamining.preprocessing import count_hifen
from datamining.preprocessing import count_slash
from datamining.preprocessing import count_question
from datamining.preprocessing import count_equals
from datamining.preprocessing import count_excla

from flask_cors import CORS
from flask import request
from flask import jsonify
from flask import Flask
from numpy import array
from joblib import load
from os import getcwd
from os import chdir
from sys import argv
import numpy as np


app = Flask(__name__)
app.config.from_object(__name__)
CORS(app, resources={r'/*': {'origins': 'http://localhost:8080'}})

correspondences = {0: 'Benign', 1: 'Defacement', 2: 'Malware', 3: 'Phishing'}
DETECTIONS = list()


def extract_features(url):

    features = list()

    features.append(len(url))
    features.append(url_protocol(url))
    features.append(count_digits(url))
    features.append(count_dirs(url))
    features.append(first_directory(url))
    features.append(count_dots(url))
    features.append(count_hifen(url))
    features.append(count_slash(url))
    features.append(count_question(url))
    features.append(count_equals(url))
    features.append(count_excla(url))

    return array(features).reshape(1, -1)


def classify_url(url, algorithm):

    features = extract_features(url)

    try:
        classifier = load(f'{getcwd()}/models/{algorithm}_model.sav')
    except (IsADirectoryError, NotADirectoryError, FileExistsError, FileNotFoundError):
        print("Model not found or doesn't exists!")

    prediction = classifier.predict(features)[0]
    probability = np.max(classifier.predict_proba(features))

    return prediction, round(probability * 100, 2)


def cli():

    # py predict.py cli https://bujhanginamfb.github.io/taelasos/update-recovry/ XGB
    if len(argv) != 4:
        print('Incorrect execution format!')
        print(f'Usage: python3 {argv[0]} {argv[1]} <url> <algorithm_name>')
        exit(127)

    algorithm = str(argv[3]).lower()

    if algorithm != 'xgb' and algorithm != 'lr':
        print('Algorithm not available.')
        print('Available algoritms: [XGB, LR]')
        exit(128)

    url = str(argv[2])
    prediction, reliability = classify_url(url, algorithm)    

    print(f'URL: {url}\n'
          f'Classified as: {correspondences[prediction]} with {reliability}% of certainty')
    

@app.route('/', methods=['GET'])
def all_detections():
    return jsonify({
        'detections': DETECTIONS,
        'status': 'success'
    })


@app.route('/', methods=['POST'])
def url_request():

    new_url = dict()
    response_object = {'status': 'success'}

    post_data = request.get_json()
    url = post_data['URL']
    alg = str(post_data['Algorithm']).lower()
    
    prediction, reliability = classify_url(url, alg)

    response_object['Class'] = str(prediction)
    response_object['Certainty'] = str(reliability)
    algorithm = 'XGBoost' if alg == 'xgb' else 'Logistic Regression'

    new_url['URL'] = url
    new_url['Type'] = correspondences[prediction]
    new_url['Probability'] = f'{reliability}%'
    new_url['Algorithm'] = algorithm

    DETECTIONS.append(new_url)

    return jsonify(response_object)


if __name__ == '__main__':

    chdir('..')
    mode = str(argv[1]).lower()

    if mode == 'cli':
        cli()
    elif mode == 'server':
        app.run()
    else:
        print('Execution mode not available.')
        print('Available modes: [CLI, SERVER]')
        exit(129)
