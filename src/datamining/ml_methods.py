from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from joblib import dump


def holdout_split(attributes, classes):

    # Training and test sets splitting (80% and 20% - holdout)
    training_attributes, test_attributes, training_classes, test_classes = train_test_split(attributes,
                                                                                            classes,
                                                                                            test_size=0.2,
                                                                                            random_state=0)
    
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
