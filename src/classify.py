"""
Created on Mon Apr 24 07:15:05 2017

@author: DETJENS2
"""

from collections import Counter
from random import randrange

import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble.weight_boosting import AdaBoostClassifier
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier
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

    
def predict(model, signal_matrix, verbose=1):
    """Predict current location, including classifier voting."""
    # TODO: classify based on *balanced* sample (repeated sampling strategy)
    for model in classifiers.values():
        model.fit(x, y.values.ravel())
     
    locations = []
    for key in classifiers.keys():
        model = classifiers[key]
        location = model.predict(signal_matrix)[0]
        if verbose > 0:
            print('Model "%s": %s' % (key, location))
        locations.append(location)

    # get most frequent prediction
    count = Counter(locations)
    max_count = max(count.values())
    max_locations = []
    for key in count.keys():
        value = count[key]
        if value == max_count:
            max_locations.append(key)
    rand_index = randrange(0,len(max_locations))
    max_location = max_locations[rand_index]
    
    if verbose > 0:
        print('Hard voting result: %s' % max_location)    
    return max_location
 
    
def classify_current_signal():
    """Predict location label for current wifi signals."""
    signal_matrix = get_signal_matrix()
    return predict(classifiers['KNN'], signal_matrix)


def stream_location():
    """Continuously predict current location."""
    while True:
        print('PreLocation: %s \n' % classify_current_signal())
        time.sleep(3)

    
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