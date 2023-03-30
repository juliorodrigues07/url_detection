import matplotlib.pyplot as plt
import seaborn as sns


def plot_distribution(dataset):

    # Statistical summary (mean, minimum, maximum, standard deviation, quartiles, ...)
    # print(url_data.describe().transpose())

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


def feature_dist(dataset, key):

    sns.countplot(x=key, data=dataset, palette='Greens')
    plt.show()
