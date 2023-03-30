from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from joblib import dump
import xgboost as xgb


def holdout_split(attributes, classes):

    # Training and test sets splitting (80% and 20% - holdout)
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
    print(classification_report(test_classes, predictions, target_names=class_names))


def svm_model(training_attributes, test_attributes, training_classes, test_classes, class_names):

    classifier = SVC(kernel='rbf', gamma=0.01, C=2)
    classifier.fit(training_attributes, training_classes)
        
    predictions = classifier.predict(test_attributes)
    print(classification_report(test_classes, predictions, target_names=class_names))


def xgb_classification(training_attributes, test_attributes, training_classes, test_classes, class_names):

    # TODO: Ensemble method: essential to aplly fine hiperparameters tuning with tripartite
    xgb_clf = xgb.XGBClassifier(base_score=0.5,
                                booster='gbtree',
                                n_estimators=500,
                                n_jobs=-1,
                                objective='reg:squarederror',
                                max_depth=5,
                                learning_rate=0.5)
    
    xgb_clf.fit(training_attributes, training_classes)
    predictions = xgb_clf.predict(test_attributes)
    print(classification_report(test_classes, predictions, target_names=class_names))

# TODO: Save trained models after tuning