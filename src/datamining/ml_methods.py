from datamining.data_visualization import plot_feature_importance
from datamining.data_visualization import calculate_importances

from sklearn.inspection import permutation_importance
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.metrics import classification_report
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
from mlxtend.evaluate import paired_ttest_5x2cv
from xgboost import XGBClassifier
from joblib import dump
from os import getcwd
import matplotlib.pyplot as plt


def holdout_split(attributes, classes):

    # Training and test sets obtained by stratified and random splitting (80% and 20% - holdout)
    training_attributes, test_attributes, training_classes, test_classes = train_test_split(attributes,
                                                                                            classes,
                                                                                            stratify=classes,
                                                                                            test_size=0.3,
                                                                                            shuffle=True,
                                                                                            random_state=42)
    
    return training_attributes, test_attributes, training_classes, test_classes


def logistic_regression(training_attributes, test_attributes, training_classes, test_classes, class_names):

    lr_clf = LogisticRegression(n_jobs=-1)

    lr_clf.fit(training_attributes, training_classes)
    predictions = lr_clf.predict(test_attributes)

    summary(class_names, test_classes, predictions, 'LR')
    dump(lr_clf, f'{getcwd()}/models/inital_lr_model.sav')

    perm_importance = permutation_importance(lr_clf, test_attributes, test_classes)
    return perm_importance


def xgb_classification(training_attributes, test_attributes, training_classes, test_classes, class_names):

    xgb_clf = XGBClassifier(booster='gbtree',
                            n_estimators=200,
                            n_jobs=-1,
                            objective='reg:squarederror',
                            max_depth=9,
                            learning_rate=0.3,
                            verbosity=1)
    
    xgb_clf.fit(training_attributes, training_classes)
    predictions = xgb_clf.predict(test_attributes)

    summary(class_names, test_classes, predictions, 'XGBoost')
    dump(xgb_clf, f'{getcwd()}/models/inital_xgb_model.sav')

    return xgb_clf.feature_importances_


def knn_classifier(training_attributes, test_attributes, training_classes, test_classes, class_names):

    knn_clf = KNeighborsClassifier(algorithm='ball_tree', n_neighbors=7, weights='distance', n_jobs=-1)

    knn_clf.fit(training_attributes, training_classes)
    predictions = knn_clf.predict(test_attributes)

    summary(class_names, test_classes, predictions, 'KNN')
    dump(knn_clf, f'{getcwd()}/models/inital_knn_model.sav')

    perm_importance = permutation_importance(knn_clf, test_attributes, test_classes)
    return perm_importance


def holdout_learning(attributes, classes, feature_names, class_names, algorithm):

    training_attributes, test_attributes, training_classes, test_classes = holdout_split(attributes, classes)

    if algorithm == 'XGB':
        f_importances = xgb_classification(training_attributes, test_attributes,
                                           training_classes, test_classes, class_names).tolist()

        # Plots XGBoost feature importance (needs skiping in normalization stage to work)
        plot_feature_importance(test_attributes.columns, training_attributes.columns, f_importances)

    elif algorithm == 'KNN':
        f_importances = knn_classifier(training_attributes, test_attributes,
                                       training_classes, test_classes, class_names)

        calculate_importances(f_importances, feature_names, 'KNN')

    elif algorithm == 'LR':
        f_importances = logistic_regression(training_attributes, test_attributes,
                                            training_classes, test_classes, class_names)

        calculate_importances(f_importances, feature_names, 'LR')

    else:
        print('Algorithm not available or incorretly specified!')
        exit(127)


def cv_learning(attributes, classes, algoritm):

    if algoritm == 'XGBoost':
        classifier = XGBClassifier(booster='gbtree',
                                   n_estimators=200,
                                   n_jobs=-1,
                                   objective='reg:squarederror',
                                   max_depth=9,
                                   learning_rate=0.3)

    elif algoritm == 'KNN':
        classifier = KNeighborsClassifier(algorithm='ball_tree', n_neighbors=7, weights='distance', n_jobs=-1)

    elif algoritm == 'LR':
        classifier = LogisticRegression(solver='lbfgs', max_iter=100, n_jobs=-1)

    else:
        print('Algorithm not available or incorretly specified!')
        exit(127)

    # Stratified k-fold cv to maintain dataset classes distribution in each set
    scores = cross_val_score(estimator=classifier, X=attributes, y=classes,
                             cv=StratifiedKFold(n_splits=10, shuffle=True, random_state=42),
                             scoring='f1_macro', n_jobs=-1, verbose=1)

    print(f'F1 Score Mean: {scores.mean()}')
    print(f'F1 Score StD:  {scores.std()}')


def fine_tuning(attributes, classes, algorithm):

    param_grid = list()

    if algorithm == 'XGB':
        param_grid = [
            {'n_estimators': [50, 100, 200], 'max_depth': [3, 5, 7, 9], 'learning_rate': [0.05, 0.1, 0.3]},
        ]
        classifier = XGBClassifier(n_jobs=-1)

    elif algorithm == 'KNN':
        param_grid = [
            {'n_neighbors': [3, 5, 7, 9, 12], 'weights': ['uniform', 'distance'], 'algorithm': ['ball_tree', 'kd_tree']},
        ]
        classifier = KNeighborsClassifier(n_jobs=-1)

    elif algorithm == 'LR':
        param_grid = [
            {'max_iter': [100, 200, 300], 'solver': ['lbfgs', 'newton-cg', 'newton-cholesky', 'sag', 'saga']},
        ]
        classifier = LogisticRegression(n_jobs=-1)

    else:
        print('Algorithm not available or incorretly specified!')
        exit(127)

    grid_search = GridSearchCV(estimator=classifier,
                               param_grid=param_grid,
                               scoring="neg_mean_squared_error",
                               n_jobs=-1,
                               cv=5,
                               verbose=1,
                               return_train_score=True)
    grid_search.fit(attributes, classes)

    print(grid_search.best_params_)
    with open(f'{getcwd()}/models/params/{algorithm}_best_params.txt', 'w') as file:
        for key in grid_search.best_params_:
            file.write(f'{key}: {grid_search.best_params_[key]}\n')


def summary(class_names, test_classes, predictions, algorithm):

    print(classification_report(test_classes, predictions, target_names=class_names))

    ConfusionMatrixDisplay.from_predictions(test_classes, predictions,
                                            display_labels=class_names, cmap='Blues', xticks_rotation='vertical')

    plt.title(f'Confusion Matrix ({algorithm})')
    plt.xlabel('Predictions')
    plt.ylabel('Real Class')

    plt.savefig(f'{getcwd()}/plots/confusion_matrix({algorithm}).svg', format='svg')
    plt.show()


def paired_ttest(classifier1, classifier2, attributes, classes):

    alpha = 0.05
    _, p = paired_ttest_5x2cv(classifier1, classifier2, attributes, classes)

    print(f'alpha:       {alpha}')
    print(f'p value:     {p}')

    if p > alpha:
        print('Models are statistically equal (Fail to reject null hypothesis)')
    else:
        print('Models statistically different (Reject null hypothesis)')
