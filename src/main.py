from datamining.data_visualization import plot_distribution
from datamining.data_visualization import protocol_dist
from datamining.preprocessing import discretize_values
from datamining.preprocessing import url_protocol
from datamining.ml_methods import holdout_split
from datamining.ml_methods import decision_tree
from datamining.ml_methods import svm_model

from warnings import filterwarnings
from pandas import read_csv
from os.path import isdir
from os import getcwd
from os import chdir
from os import mkdir


filterwarnings('ignore')
chdir('..')
if not isdir(f'{getcwd()}/models'):
    mkdir(f'{getcwd()}/models')


def main():
    
    url_dataset = read_csv(f'{getcwd()}/datasets/test.csv')
    class_names = ['benign', 'defacement', 'phishing', 'malware']

    # plot_distribution(url_dataset)

    attributes = url_dataset.drop(['type'], axis='columns')
    attributes = discretize_values(attributes.copy(), 'url')

    classes = url_dataset.drop(['url'], axis='columns') 
    classes = discretize_values(classes.copy(), 'type')

    # url_dataset['protocol'] = url_dataset['url'].apply(lambda x: url_protocol(x))
    # attributes = url_dataset.drop(['type'], axis='columns')
    # attributes = discretize_values(attributes.copy(), 'url')
    # attributes = discretize_values(attributes.copy(), 'protocol')

    # protocol_dist(url_dataset)

    training_attributes, test_attributes, training_classes, test_classes = holdout_split(attributes, classes)
    decision_tree(training_attributes, test_attributes, training_classes, test_classes, class_names)

    training_attributes, test_attributes, training_classes, test_classes = holdout_split(attributes, classes)
    svm_model(training_attributes, test_attributes, training_classes, test_classes, class_names)


if __name__ == '__main__':
    main()
