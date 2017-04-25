# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 07:15:05 2017

@author: DETJENS2
"""

import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble.weight_boosting import AdaBoostClassifier
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

from windows import get_feature_matrix, get_labels, get_signal_matrix


# historial data
x = get_feature_matrix()
y = get_labels()
# define models
classifiers = {'KNN': KNeighborsClassifier(n_neighbors=3, algorithm='auto',
                                           metric='braycurtis'),
               'RandForest': RandomForestClassifier(n_estimators=80, n_jobs=1),
               #'SVM': SVC(gamma=2, C=1),
               #'linear SVM': SVC(kernel="linear", C=0.025),
               'DecisionTree': DecisionTreeClassifier(max_depth=5),
               'AdaBoost': AdaBoostClassifier(n_estimators=80, learning_rate=0.4),
               #'Naive Bayes': GaussianNB(),
               }


def evaluate_model(model_name, model, x, y):
    """Evaluate model accuracy via cross validation."""
    print('%s:' % model_name)
    model.fit(x, y.values.ravel())
    print('CV f1_micro (not reusing data): %s' % np.mean(cross_val_score(model, x, 
          y.values.ravel(), cv=5, scoring='f1_micro')))

    
def predict(model, signal_matrix):
    """Predict current location, including classifier voting."""
    model.fit(x, y.values.ravel())
    return model.predict(signal_matrix)[0]
    
    # TODO: combine classifiers
    #vc = VotingClassifier(classifiers.items(), n_jobs=1)
    #evaluate_model('VotingClassifier', vc, x, y)    

    
def classify_current_signal():
    """Predict location label for current wifi signals."""
    signal_matrix = get_signal_matrix()
    return predict(classifiers['KNN'], signal_matrix)
    
           
if __name__ == '__main__':
#    x = get_feature_matrix()
#    print(x)
#    s = signals_windows()
#    print(s)
    # evaluate models
#    for name in classifiers.keys():
#        evaluate_model(name, classifiers[name], x, y)        
    # predict current position
    location = classify_current_signal()
    print(location)