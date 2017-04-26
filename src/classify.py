"""
Created on Mon Apr 24 07:15:05 2017

@author: DETJENS2
"""

from random import randrange

import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.ensemble.weight_boosting import AdaBoostClassifier
from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

import time

from database import get_feature_matrix, get_labels, get_signal_matrix


# historial data
x = get_feature_matrix()
y = get_labels()
# define models
classifiers = {'KNN': KNeighborsClassifier(n_neighbors=3, algorithm='auto',
                                           metric='braycurtis'),
               'RandForest': RandomForestClassifier(n_estimators=80, n_jobs=1),
               #'SVM': SVC(gamma=2, C=1),
               'linear SVM': SVC(kernel="linear", C=0.025),
               'DecisionTree': DecisionTreeClassifier(max_depth=5),
               'AdaBoost': AdaBoostClassifier(n_estimators=80, learning_rate=0.4),
               'Naive Bayes': GaussianNB(),
               }

vc = VotingClassifier(estimators=list(classifiers.items()), voting='hard')


def evaluate_model(model_name, model, x, y):
    """Evaluate model accuracy via cross validation."""
    print('%s:' % model_name)
    model.fit(x, y.values.ravel())
    print('CV f1_micro (not reusing data): %s' % np.mean(cross_val_score(model, x, 
          y.values.ravel(), cv=5, scoring='f1_micro')))


def evaluate_all_models():
    """Evalate all models via cross validation."""
    # evaluate models
    for name in classifiers.keys():
        evaluate_model(name, classifiers[name], x, y)   
    evaluate_model('VotingClassifier', vc, x, y)
    # TODO: evaluate voting classifier, following demo_VotingClassifier.py


def predict(signal_matrix, verbose=1):
    """Predict current location, based on hard voting among ensemble of classifiers."""
    # TODO: classify based on *balanced* sample (repeated sampling strategy)        
    # report for models within VotingClassifier
    for key in classifiers.keys():
        model = classifiers[key]
        model.fit(x, y.values.ravel())        
        location = model.predict(signal_matrix)[0]
        if verbose > 0:
            print('Model "%s": %s' % (key, location))
    # report for VotingClassifier
    vc.fit(x, y.values.ravel())
    vc_locations = vc.predict(signal_matrix)
    # in case VotingClassifier returns more than one result: always draw random element
    rand_index = randrange(0,len(vc_locations))
    vc_location = vc_locations[rand_index]
    if verbose > 0:
        print('VotingClassifier result: %s' % vc_location)
    return vc_location
 
    
def classify_current_signal():
    """Predict location label for current wifi signals."""
    signal_matrix = get_signal_matrix()
    return predict(signal_matrix)


def stream_location():
    """Continuously predict current location."""
    while True:
        print('PreLocation: %s \n' % classify_current_signal())
        time.sleep(3)

    
if __name__ == '__main__':
    # evaluate_all_models()
    classify_current_signal()
    #stream_location()