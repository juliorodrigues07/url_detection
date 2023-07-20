# Local source code
from datamining.data_visualization import plot_correlation_matrix
from datamining.data_visualization import plot_distribution
from datamining.data_visualization import url_len_boxplot
from datamining.data_visualization import dataset_stats
from datamining.data_visualization import feature_dist
from datamining.data_visualization import pie_chart

from datamining.preprocessing import majority_undersampling
from datamining.preprocessing import minority_oversampling
from datamining.preprocessing import discretize_values
from datamining.preprocessing import feature_selection
from datamining.preprocessing import count_punctuation
from datamining.preprocessing import count_underscore
from datamining.preprocessing import count_commercial
from datamining.preprocessing import first_directory
from datamining.preprocessing import count_question
from datamining.preprocessing import normalization
from datamining.preprocessing import count_percent
from datamining.preprocessing import count_hashtag
from datamining.preprocessing import count_cipher
from datamining.preprocessing import url_protocol
from datamining.preprocessing import count_digits
from datamining.preprocessing import count_equals
from datamining.preprocessing import count_hifen
from datamining.preprocessing import count_slash
from datamining.preprocessing import count_excla
from datamining.preprocessing import count_dirs
from datamining.preprocessing import url_length
from datamining.preprocessing import count_dots
from datamining.preprocessing import count_plus
from datamining.preprocessing import count_star
from datamining.preprocessing import odd_words
from datamining.preprocessing import count_ats

from datamining.ml_methods import holdout_learning
from datamining.ml_methods import paired_ttest
from datamining.ml_methods import cv_learning
from datamining.ml_methods import fine_tuning

# External libraries
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from warnings import filterwarnings
from xgboost import XGBClassifier
from pandas import read_csv
from os.path import isdir
from os import getcwd
from os import chdir
from os import mkdir


filterwarnings('ignore')
chdir('..')
if not isdir(f'{getcwd()}/plots'):
    mkdir(f'{getcwd()}/plots')
if not isdir(f'{getcwd()}/plots/features'):
    mkdir(f'{getcwd()}/plots/features')
if not isdir(f'{getcwd()}/models'):
    mkdir(f'{getcwd()}/models')
if not isdir(f'{getcwd()}/models/params'):
    mkdir(f'{getcwd()}/models/params')


def analyze_dataset(dataset, class_names):

    # Plots classes distribution
    plot_distribution(dataset)
    pie_chart(dataset, class_names)

    # Plots the selected feature distribution between instances in the dataset
    feature_dist(dataset, 'protocol')

    # Boxplot to identify URLs which are outliers in length
    url_len_boxplot(dataset)

    # Statistical data and features correlation in the dataset
    dataset_stats(dataset)
    plot_correlation_matrix(dataset, 8)


def balance_dataset(attributes, classes):

    # Undersamples benign instances
    under_att, under_cls = majority_undersampling(attributes.copy(), classes.copy())

    # Oversamples defacement and malware instances
    balanced_attributes, balanced_classes = minority_oversampling(under_att, under_cls)

    balanced_attributes['type'] = balanced_classes
    balanced_attributes.to_csv(f'{getcwd()}/datasets/balanced_v2.csv', index=False)

    return balanced_attributes, balanced_classes


def grind_dataset(dataset):

    # TODO: Merge classes? {defacement, phishing, malware} ==> malicious

    url_dataset = url_length(dataset)
    url_dataset['protocol'] = url_dataset['url'].apply(lambda x: url_protocol(x))
    url_dataset['digits_qtd'] = url_dataset['url'].apply(lambda x: count_digits(x))
    url_dataset['dirs_qtd'] = url_dataset['url'].apply(lambda x: count_dirs(x))
    url_dataset['fstdir_length'] = url_dataset['url'].apply(lambda x: first_directory(x))
    url_dataset['dots'] = url_dataset['url'].apply(lambda x: count_dots(x))
    url_dataset['hifens'] = url_dataset['url'].apply(lambda x: count_hifen(x))
    url_dataset['slash'] = url_dataset['url'].apply(lambda x: count_slash(x))
    url_dataset['question'] = url_dataset['url'].apply(lambda x: count_question(x))
    url_dataset['equals'] = url_dataset['url'].apply(lambda x: count_equals(x))
    url_dataset['exclamation'] = url_dataset['url'].apply(lambda x: count_excla(x))

    # Discarded features
    url_dataset['susp_words'] = url_dataset['url'].apply(lambda x: odd_words(x))
    url_dataset['underscore'] = url_dataset['url'].apply(lambda x: count_underscore(x))
    url_dataset['ats'] = url_dataset['url'].apply(lambda x: count_ats(x))
    url_dataset['commercial'] = url_dataset['url'].apply(lambda x: count_commercial(x))
    url_dataset['plus'] = url_dataset['url'].apply(lambda x: count_plus(x))
    url_dataset['star'] = url_dataset['url'].apply(lambda x: count_star(x))
    url_dataset['hashtag'] = url_dataset['url'].apply(lambda x: count_hashtag(x))
    url_dataset['cipher'] = url_dataset['url'].apply(lambda x: count_cipher(x))
    url_dataset['percent'] = url_dataset['url'].apply(lambda x: count_percent(x))
    url_dataset = count_punctuation(url_dataset.copy())

    # Saves the recently preprocessed dataset
    url_dataset.to_csv(f'{getcwd()}/datasets/preprocessed_v2.csv', index=False)
    return url_dataset


def main():

    # Merged Kaggle dataset with PhishTank dataset, excluding any duplicates
    # url_dataset = read_csv(f'{getcwd()}/datasets/merged.csv')
    # polished_dataset = grind_dataset(url_dataset)

    polished_dataset = read_csv(f'{getcwd()}/datasets/final.csv')

    class_names = ['Benign', 'Defacement', 'Phishing', 'Malware']
    feature_names = list(polished_dataset.columns.values)
    feature_names.remove('type')

    # First impressions of the dataset
    # analyze_dataset(polished_dataset, class_names)

    # Splits the dataset between instances' attributes and its class
    attributes = polished_dataset.drop(['type'], axis='columns')
    classes = discretize_values(polished_dataset.copy(), 'type')['type']

    # Normalizes the attributes' values (Z-Score)
    attributes = normalization(attributes.copy())

    # Applies recursive feature selection with XGBoost (needs skiping in normalization stage to work)
    # feature_selection(attributes, classes)

    # Balancing the dataset (200k each class)
    # attributes, classes = balance_dataset(attributes.copy(), classes.copy())

    # Learning with desired ML algorithm, apllying holdout train/test split
    holdout_learning(attributes, classes, feature_names, class_names, 'LR')

    # Learning with desired ML algorithm, apllying k-fold cross validation
    cv_learning(attributes, classes, 'LR')

    # Applies fine-tuning with the desired ML algorithm
    # fine_tuning(attributes, classes, 'LR')

    # PAIRED T TEST #
    # classifier1 = XGBClassifier(booster='gbtree',
    #                             n_estimators=200,
    #                             n_jobs=-1,
    #                             objective='reg:squarederror',
    #                             max_depth=9,
    #                             learning_rate=0.3)
    # classifier2 = LogisticRegression(solver='lbfgs', max_iter=100, n_jobs=-1)
    # classifier3 = KNeighborsClassifier(algorithm='ball_tree', n_neighbors=7, weights='distance', n_jobs=-1)

    # paired_ttest(classifier1, classifier3, attributes, classes)


if __name__ == '__main__':
    main()
