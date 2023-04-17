from sklearn.preprocessing import LabelEncoder
from urllib.parse import urlparse
import re


def discretize_values(column, key):

    encoding = LabelEncoder()

    # Discretize column values (bening, phishing, malware, ...) => [0, 1, 2, ...]
    encoding.fit(column[key])
    column[key] = encoding.transform(column[key].copy())

    return column


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
