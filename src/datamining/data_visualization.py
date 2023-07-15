import matplotlib.pyplot as plt
import seaborn as sns
from pandas import DataFrame
from numpy import array


def plot_distribution(dataset):

    # Statistical summary (mean, minimum, maximum, standard deviation, quartiles, ...)
    # print(dataset.describe().transpose())

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

    # fig.savefig()


def pie_chart(dataset, names):

    colors = sns.color_palette('pastel')[0:5]
    split = dataset.type.value_counts()
    plt.pie(split, colors=colors, shadow=True, startangle=45, autopct='%.0f%%')

    plt.title('Class Distribution')
    plt.legend(names, loc="best")
    plt.axis('equal')
    plt.show()


def feature_dist(dataset, key):

    # plt.title('Protocol')
    sns.countplot(x=key, data=dataset, palette='Blues')
    plt.ylabel('Instances')
    plt.show()


def url_len_boxplot(dataset):

    fig, axes = plt.subplots(figsize=(18, 10))
    sns.boxplot(ax=axes, x='type', y='url_length', data=dataset)

    axes.set_title('URL lengths between each type')
    axes.set_xlabel('URL Length')
    axes.set_xlabel('Type')
    plt.show()


def plot_feature_importance(cols, feature_dataframe):

    feature_data = DataFrame({'Feature': cols, 'Feature Relevance': feature_dataframe['Mean'].values})
    feature_data = feature_data.sort_values(by='Feature Relevance', ascending=False)

    plt.figure(figsize=(10, 12))
    plt.title('Average Feature Importance', fontsize=14)

    s = sns.barplot(y='Feature', x='Feature Relevance', data=feature_data, orient='h', palette='coolwarm')
    s.set_xticklabels(s.get_xticklabels(), rotation=90)

    plt.show()


def calculate_importances(perm_importances, features_names):

    features = array(features_names)
    sorted_idx = perm_importances.importances_mean.argsort()

    plt.barh(features[sorted_idx], perm_importances.importances_mean[sorted_idx])
    plt.title('Permutation Feature Importance')
    plt.ylabel('Feature')
    plt.xlabel("Feature Relevance")

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
    plt.show()
