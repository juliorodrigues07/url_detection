import matplotlib.pyplot as plt
import seaborn as sns
from pandas import DataFrame
from numpy import arange
from numpy import array
from os import getcwd


def dataset_stats(dataset):

    # Statistical data (min, max, mean, std, quartiles...) and features mean values by associated class
    print(dataset.isna().sum())
    print(dataset.describe().transpose())

    # {0, 1, 2, 3} ==> {benign, defacement, phishing, malware}
    print(dataset.groupby('type').mean().loc[3])


def plot_distribution(dataset):

    split = dataset.type.value_counts()

    fig, ax = plt.subplots(figsize=(12, 8))
    sns.barplot(x=split.index, y=split, palette='Reds')

    ax.set_title('Class Distribution')
    ax.set_ylabel("Amount", fontsize=18)
    ax.set_xlabel("URL Types", fontsize=18)

    ax.grid(which='both')
    ax.grid(which='minor', alpha=0.8)
    ax.grid(which='major', alpha=0.8)
    plt.show()

    fig.savefig(f'{getcwd()}/plots/class_dist(bar).svg', format='svg')


def pie_chart(dataset, names):

    colors = sns.color_palette('pastel')[0:5]
    split = dataset.type.value_counts()
    plt.pie(split, colors=colors, shadow=True, startangle=45, autopct='%.0f%%')

    plt.title('Class Distribution')
    plt.legend(names, loc="best")
    plt.axis('equal')

    plt.savefig(f'{getcwd()}/plots/class_dist(pie).svg', format='svg')
    plt.show()


def feature_dist(dataset, key):

    # plt.title('Protocol')
    sns.countplot(x=key, data=dataset, palette='Blues')
    plt.ylabel('Instances')

    plt.savefig(f'{getcwd()}/plots/features/feat_dist({key}).svg', format='svg')
    plt.show()


def url_len_boxplot(dataset):

    fig, axes = plt.subplots(figsize=(18, 10))
    sns.boxplot(ax=axes, x='type', y='url_length', data=dataset)

    axes.set_title('URL lengths between each type')
    axes.set_xlabel('URL Length')
    axes.set_xlabel('Type')
    plt.show()

    fig.savefig(f'{getcwd()}/plots/url_len(boxplot).svg', format='svg')


def plot_feature_importance(cols, attributes, f_importances):

    feature_dataframe = DataFrame({'Feature': attributes, 'Feature Relevance': f_importances})
    feature_dataframe['Mean'] = feature_dataframe.mean(axis=1)

    feature_data = DataFrame({'Feature': cols, 'Feature Relevance': feature_dataframe['Mean'].values})
    feature_data = feature_data.sort_values(by='Feature Relevance', ascending=False)

    plt.figure(figsize=(10, 12))
    plt.title('Average Feature Importance (XGBoost)', fontsize=14)

    s = sns.barplot(y='Feature', x='Feature Relevance', data=feature_data, orient='h', palette='coolwarm')
    s.set_xticklabels(s.get_xticklabels(), rotation=90)

    plt.savefig(f'{getcwd()}/plots/features/feat_importance(XGBoost).svg', format='svg')
    plt.show()


def calculate_importances(perm_importances, features_names, algorithm):

    features = array(features_names)
    sorted_idx = perm_importances.importances_mean.argsort()

    plt.barh(features[sorted_idx], perm_importances.importances_mean[sorted_idx])
    plt.title(f'Permutation Feature Importance ({algorithm})')
    plt.ylabel('Feature')
    plt.xlabel("Feature Relevance")

    plt.savefig(f'{getcwd()}/plots/features/feat_importance({algorithm}).svg', format='svg')
    plt.show()


def plot_correlation_matrix(df, graph_width):

    df = df.dropna('columns')
    df = df[[col for col in df if df[col].nunique() > 1]]

    if df.shape[1] < 2:
        return

    corr = df.corr()
    plt.figure(num=None, figsize=(graph_width, graph_width), dpi=80, facecolor='w', edgecolor='k')
    corr_mat = plt.matshow(corr, fignum=1)

    plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)
    plt.yticks(range(len(corr.columns)), corr.columns)
    plt.gca().xaxis.tick_bottom()
    plt.colorbar(corr_mat)
    plt.title(f'Correlation Matrix', fontsize=15)

    plt.savefig(f'{getcwd()}/plots/correlation_matrix.svg', format='svg')
    plt.show()


def plot_selected_features(n_features, f_importances, attributes):

    plt.figure(figsize=(8, 8))
    plt.barh(range(n_features), f_importances, align='center')
    plt.yticks(arange(n_features), attributes)

    plt.title('Selected Features')
    plt.xlabel('Feature importance')
    plt.ylabel('Feature')

    plt.savefig(f'{getcwd()}/plots/features/selected_feat.svg', format='svg')
    plt.show()
