from imblearn.under_sampling import RandomUnderSampler
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE
from urllib.parse import urlparse
import re


def discretize_values(dataset, column):

    encoding = LabelEncoder()

    # Discretize dataset values (bening, phishing, malware, ...) => [0, 1, 2, ...]
    encoding.fit(dataset[column])
    dataset[column] = encoding.transform(dataset[column].copy())

    return dataset


def url_protocol(url):
    
    protocol = urlparse(url).scheme

    # Identifying which communication protocol each site uses
    match = str(protocol)
    if match == 'https':
        return 2
    elif match == 'http':
        return 0
    else:
        return 1


def url_length(dataset):

    # Gets the brute length of each url
    dataset['url_length'] = dataset['url'].apply(lambda x: len(x))
    return dataset


def count_digits(url):

    total = 0

    # Counts the number of digits present in each url
    for c in url:
        if c.isnumeric():
            total += 1

    return total


def count_dirs(url):

    # Counts the number of directories present in each url path
    url_path = urlparse(url).path
    return url_path.count('/')


def count_punctuation(dataset):

    aux = dataset.copy()
    aux['url_alphas'] = aux['url'].apply(lambda i: count_alpha(i))

    dataset['url_punc'] = dataset['url_length'] - dataset['digits_qtd'] - aux['url_alphas']
    return dataset


def first_directory(url):

    url_path = urlparse(url).path

    # Gets the brute length of each url first directory
    try:
        fd_length = len(url_path.split('/')[1])
    except IndexError:
        fd_length = 0

    return fd_length


def odd_words(url):

    # Search for suspicious words related to phishing in each url
    pattern = re.search('free|account|signin|bonus|lucky|extra|payment|details', url)

    if pattern:
        return 1
    else:
        return 0


def count_alpha(url):

    alpha_numerics = 0

    for c in url:
        if c.isalpha():
            alpha_numerics += 1

    return


def majority_undersampling(attributes, classes):

    # Benign instances (encoded as 0) randomly removed to achieve approximately 200k
    undersampler = RandomUnderSampler(sampling_strategy={0: 200211})
    x_after, y_after = undersampler.fit_resample(attributes, classes)

    return x_after, y_after


def minority_oversampling(attributes, classes):

    oversampler = SMOTE()
    x_after, y_after = oversampler.fit_resample(attributes, classes)
    
    return x_after, y_after
