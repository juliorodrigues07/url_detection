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

from numpy import array
from joblib import load
from os import getcwd
from os import chdir
from sys import argv


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


def main():

    if len(argv) != 3:
        print('Incorrect execution format!')
        print(f'Usage: python3 {argv[0]} <url> <algorithm_name>')
        exit(127)

    algotithm = str(argv[2])

    if algotithm.lower() != 'xgb' and algotithm.lower() != 'lr':
        print('Algorithm not available.')
        print('Available algoritms: [XGB, LR]')
        exit(127)

    url = str(argv[1])
    features = extract_features(url)

    classifier = load(f'{getcwd()}/models/{algotithm.lower()}_model.sav')
    prediction = classifier.predict(features)[0]

    correspondences = {0: 'Benign', 1: 'Defacement', 2: 'Malware', 3: 'Phishing'}
    print(f'URL: {url}\n'
          f'Classified as: {correspondences[prediction]}')


if __name__ == '__main__':
    chdir('..')
    main()
