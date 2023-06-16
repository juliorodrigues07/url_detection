# Local source code
from datamining.data_visualization import plot_feature_importance
from datamining.data_visualization import calculate_importances
from datamining.data_visualization import plot_distribution
from datamining.data_visualization import url_len_boxplot
from datamining.data_visualization import feature_dist
from datamining.data_visualization import pie_chart
from datamining.preprocessing import majority_undersampling
from datamining.preprocessing import minority_oversampling
from datamining.preprocessing import discretize_values
from datamining.preprocessing import count_punctuation
from datamining.preprocessing import first_directory
from datamining.preprocessing import url_protocol
from datamining.preprocessing import count_digits
from datamining.preprocessing import count_dirs
from datamining.preprocessing import url_length
from datamining.preprocessing import url_status
from datamining.preprocessing import odd_words
from datamining.ml_methods import logistic_regression
from datamining.ml_methods import xgb_classification
from datamining.ml_methods import holdout_split
from datamining.ml_methods import paired_ttest
from datamining.ml_methods import cv_learning

# External libraries
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from warnings import filterwarnings
from xgboost import XGBClassifier
from pandas import DataFrame
from pandas import read_csv
from os.path import isdir
from os import getcwd
from os import chdir
from os import mkdir


filterwarnings('ignore')
chdir('..')
if not isdir(f'{getcwd()}/models'):
    mkdir(f'{getcwd()}/models')


def ds_stats(dataset):

    # Statistical data (min, max, mean, std, quartiles...) and features mean values by associated class
    print(dataset.isna().sum())
    print(dataset.describe().transpose())
    print(dataset.groupby('type').mean().loc['malware'])


def balance_dataset(attributes, classes):

    # Undersamples benign instances
    under_att, under_cls = majority_undersampling(attributes.copy(), classes.copy())

    # Oversamples defacement and malware instances
    balanced_attributes, balanced_classes = minority_oversampling(under_att, under_cls)

    balanced_attributes['type'] = balanced_classes
    balanced_attributes.to_csv(f'{getcwd()}/datasets/balanced.csv', index=False)

    return balanced_attributes, balanced_classes


def grind_dataset(dataset):

    # TODO: Merge classes? {defacement, phishing, malware} ==> malicious

    # url_dataset = url_status(dataset) --> CAREFUL WITH THIS: POTENTIAL SECURITY AND MEMORY PROBLEMS

    url_dataset = discretize_values(dataset.copy(), 'online?')
    url_dataset = url_length(url_dataset.copy())
    url_dataset['protocol'] = url_dataset['url'].apply(lambda x: url_protocol(x))
    url_dataset['digits_qtd'] = url_dataset['url'].apply(lambda x: count_digits(x))
    url_dataset['dirs_qtd'] = url_dataset['url'].apply(lambda x: count_dirs(x))
    url_dataset['fstdir_length'] = url_dataset['url'].apply(lambda x: first_directory(x))
    url_dataset['susp_words'] = url_dataset['url'].apply(lambda x: odd_words(x))
    url_dataset = count_punctuation(url_dataset.copy())

    # Saves the recently preprocessed dataset
    url_dataset.to_csv(f'{getcwd()}/datasets/preprocessed_v2.csv', index=False)
    return url_dataset


def main():

    # Merged Kaggle dataset with PhishTank dataset, excluding any duplicates
    # url_dataset = read_csv(f'{getcwd()}/datasets/merged.csv')
    # polished_dataset = grind_dataset(url_dataset)

    polished_dataset = read_csv(f'{getcwd()}/datasets/balanced.csv')
    class_names = ['Benign', 'Defacement', 'Phishing', 'Malware']
    feature_names = ['online?', 'url_length', 'protocol', 'digits_qtt', 'dirs_qtt', 'fstdir_len', 'susp_words', 'url_punc']

    # Plots classes distribution
    # plot_distribution(polished_dataset)
    # pie_chart(polished_dataset, class_names)

    # Plots the selected feature distribution between instances in the dataset
    # feature_dist(polished_dataset, 'protocol')

    # ds_stats(polished_dataset)

    attributes = polished_dataset.drop(['type'], axis='columns')
    classes = discretize_values(polished_dataset.copy(), 'type')['type']

    # attributes, classes = balance_dataset(attributes.copy(), classes.copy())

    # Normalizes the attributes' values (Z-Score)
    attr_scaler = StandardScaler()
    attributes = attr_scaler.fit_transform(attributes.copy())

    # MACHINE LEARNING MODELS #

    # training_attributes, test_attributes, training_classes, test_classes = holdout_split(attributes, classes)
    # f_importances = logistic_regression(training_attributes, test_attributes,
    #                                     training_classes, test_classes, class_names)
    # calculate_importances(f_importances, feature_names)

    # training_attributes, test_attributes, training_classes, test_classes = holdout_split(attributes, classes)
    # f_importances = xgb_classification(training_attributes, test_attributes,
    #                                    training_classes, test_classes, class_names).tolist()

    # Plots XGBoost feature importance (needs skiping in scaling stage to work)
    # cols = training_attributes.columns
    # feature_dataframe = DataFrame({'Features': cols, 'XGBoost Feature Importances': f_importances})
    # feature_dataframe['Mean'] = feature_dataframe.mean(axis=1)
    # plot_feature_importance(test_attributes.columns, feature_dataframe)

    # CROSS VALIDATION #

    # classifier = XGBClassifier(base_score=0.5,
    #                            booster='gbtree',
    #                            n_estimators=100,
    #                            n_jobs=-1,
    #                            objective='reg:squarederror',
    #                            max_depth=5,
    #                            learning_rate=0.1)
    # cv_learning(attributes, classes, classifier)

    classifier = LogisticRegression(n_jobs=-1)
    cv_learning(attributes, classes, classifier)

    # PAIRED T TEST #

    # classifier1 = XGBClassifier(base_score=0.5,
    #                            booster='gbtree',
    #                            n_estimators=100,
    #                            n_jobs=-1,
    #                            objective='reg:squarederror',
    #                            max_depth=5,
    #                            learning_rate=0.1)

    # classifier2 = LogisticRegression(n_jobs=-1)

    # paired_ttest(classifier1, classifier2, attributes, classes)


if __name__ == '__main__':
    main()
