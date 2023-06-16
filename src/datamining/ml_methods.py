from sklearn.inspection import permutation_importance
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.metrics import classification_report
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
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
                                                                                            test_size=0.2,
                                                                                            shuffle=True,
                                                                                            random_state=42)
    
    return training_attributes, test_attributes, training_classes, test_classes


def decision_tree(training_attributes, test_attributes, training_classes, test_classes, class_names):

    # Model construction with decision tree
    classifier = DecisionTreeClassifier()
    classifier.fit(training_attributes, training_classes)

    # Extraction of the obtained test results
    predictions = classifier.predict(test_attributes)
    summary(class_names, test_classes, predictions)

    return classifier.feature_importances_


def svm_model(training_attributes, test_attributes, training_classes, test_classes, class_names):

    classifier = OneVsRestClassifier(SVC(kernel='rbf', gamma=0.01, C=2), n_jobs=-1)
    classifier.fit(training_attributes, training_classes)

    predictions = classifier.predict(test_attributes)
    summary(class_names, test_classes, predictions)

    perm_importance = permutation_importance(classifier, test_attributes, test_classes)
    return perm_importance


def logistic_regression(training_attributes, test_attributes, training_classes, test_classes, class_names):

    classifier = LogisticRegression(n_jobs=-1)
    classifier.fit(training_attributes, training_classes)

    predictions = classifier.predict(test_attributes)
    summary(class_names, test_classes, predictions)

    perm_importance = permutation_importance(classifier, test_attributes, test_classes)
    return perm_importance


def xgb_classification(training_attributes, test_attributes, training_classes, test_classes, class_names):

    # TODO: Ensemble method: essential to aplly hiperparameters fine tuning with tripartite
    xgb_clf = XGBClassifier(base_score=0.5,
                            booster='gbtree',
                            n_estimators=100,
                            n_jobs=-1,
                            objective='reg:squarederror',
                            max_depth=5,
                            learning_rate=0.1)
    
    xgb_clf.fit(training_attributes, training_classes)
    predictions = xgb_clf.predict(test_attributes)

    summary(class_names, test_classes, predictions)
    # dump(xgb_clf, f'{getcwd()}/models/inital_xgb_model.sav')

    return xgb_clf.feature_importances_


def cv_learning(attributes, classes, classifier):

    # Stratified k-fold cv to maintain dataset classes distribution in each set
    scores = cross_val_score(estimator=classifier, X=attributes, y=classes,
                             cv=StratifiedKFold(n_splits=10, shuffle=True),
                             scoring='f1_macro', n_jobs=-1)

    print(f'F1 Score Mean: {scores.mean()}')
    print(f'F1 Score StD:  {scores.std()}')


def summary(class_names, test_classes, predictions):

    print(classification_report(test_classes, predictions, target_names=class_names))

    ConfusionMatrixDisplay.from_predictions(test_classes, predictions,
                                            display_labels=class_names, cmap='Blues', xticks_rotation='vertical')

    plt.title('Confusion Matrix')
    plt.xlabel('Predictions')
    plt.ylabel('Real Class')
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
