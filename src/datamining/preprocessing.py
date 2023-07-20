from datamining.data_visualization import plot_selected_features
from datamining.ml_methods import holdout_split

from imblearn.under_sampling import RandomUnderSampler
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_selection import RFECV
from imblearn.over_sampling import SMOTE
from xgboost import XGBClassifier
from urllib.parse import urlparse
from os import getcwd
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

    return alpha_numerics


def count_dots(url):
    return url.count('.')


def count_hifen(url):
    return url.count('-')


def count_underscore(url):
    return url.count('_')


def count_slash(url):
    return url.count('/')


def count_question(url):
    return url.count('?')


def count_equals(url):
    return url.count('=')


def count_ats(url):
    return url.count('@')


def count_commercial(url):
    return url.count('&')


def count_excla(url):
    return url.count('!')


def count_plus(url):
    return url.count('+')


def count_star(url):
    return url.count('*')


def count_hashtag(url):
    return url.count('#')


def count_cipher(url):
    return url.count('$')


def count_percent(url):
    return url.count('%')


def normalization(attributes):

    attr_scaler = StandardScaler()
    return attr_scaler.fit_transform(attributes)


def majority_undersampling(attributes, classes):

    # Benign instances (encoded as 0) randomly removed to achieve approximately 200k
    undersampler = RandomUnderSampler(sampling_strategy={0: 200000})
    x_after, y_after = undersampler.fit_resample(attributes, classes)

    return x_after, y_after


def minority_oversampling(attributes, classes):

    oversampler = SMOTE(sampling_strategy='not majority', n_jobs=-1)
    x_after, y_after = oversampler.fit_resample(attributes, classes)

    return x_after, y_after


def feature_selection(attributes, classes):

    # Recursive feature selection with XGBoost and CV
    cv_estimator = XGBClassifier(n_jobs=-1)
    x_train, _, y_train, _ = holdout_split(attributes, classes)
    cv_estimator.fit(x_train, y_train)

    cv_selector = RFECV(cv_estimator, cv=5, step=1, scoring='f1_macro', verbose=1, n_jobs=-1)
    cv_selector = cv_selector.fit(x_train, y_train)
    rfecv_mask = cv_selector.get_support()

    rfecv_features = list()
    for check, feature in zip(rfecv_mask, x_train.columns):
        if check:
            rfecv_features.append(feature)

    print(f'Optimal number of features: {cv_selector.n_features_}')
    print(f'Best features: {rfecv_features}')

    with open(f'{getcwd()}/datasets/best_features.txt', 'w') as file:
        file.write(f'Optimal number of features: {cv_selector.n_features_}\n')
        file.write(f'Best features: {rfecv_features}')

    attributes.drop(rfecv_features, axis='columns')
    attributes['type'] = classes
    attributes.to_csv(f'{getcwd()}/datasets/feature_selected.csv', index=False)

    n_features = x_train.shape[1]
    plot_selected_features(n_features, cv_estimator.feature_importances_, x_train.columns.values)
