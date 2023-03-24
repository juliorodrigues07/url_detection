# from datamining.data_visualization import
# from datamining.preprocessing import
# from datamining.ml_methods import

from warnings import filterwarnings
from os.path import isdir
from os import getcwd
from os import chdir
from os import mkdir
import pandas as pd


filterwarnings('ignore')
chdir('..')
if not isdir(f'{getcwd()}/models'):
    mkdir(f'{getcwd()}/models')


def main():
    
    print('Data Mining Start!')
    # url_dataset = pd.read_csv(f'{getcwd()}/datasets/URLs.csv')


if __name__ == '__main__':
    main()
