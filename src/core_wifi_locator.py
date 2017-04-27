"""
Created on Wed Apr 26 21:26:28 2017

@author: DETJENS2
"""

import time

from model_database import get_feature_matrix, get_labels, get_signal_matrix
from model_database import log_signals
from utils_wifi import get_signals
from utils_classification import predict, evaluate_model, vc, classifiers

# locations that can be logged
locations = ['traveling', 'living_room', 'kitchen', 'bedroom', 'bathroom']


def evaluate_all_models():
    """Evalate all models via cross validation."""
    # retrieve data from model
    X = get_feature_matrix()
    y = get_labels()
    # evaluate models
    for name in classifiers.keys():
        evaluate_model(name, classifiers[name], X, y)   
    evaluate_model('VotingClassifier', vc, X, y)


def predict_current_location():
    """Predict location label for current wifi signals."""
    # read from sensors
    signals = get_signals()
    # read from model
    X_train = get_feature_matrix()
    y_train = get_labels()
    X_signal = get_signal_matrix(X_train, signals)
    # classify signal
    location = predict(X_train, y_train, X_signal)
    return location


def stream_location():
    """Continuously predict current location."""
    while True:
        print('PreLocation: %s \n' % predict_current_location())
        time.sleep(3)


def log_location(verbose=1):
    """Ask for location and log it, together with current wifi signals."""
    def get_location():
        """Get location from user (options in script parameters)."""
        print('Where are you located?')
        for i in range(0, len(locations)):
            print("%i - %s" % (i, locations[i]))
        k = int(input('location: '))
        return locations[k]

    # read from sensors
    signals = get_signals()
    # read form user input
    location = get_location()
    # log location to model
    if verbose > 0:
        print('Logging location "%s" ... ' % location)
    log_signals(signals, location=location)


if __name__ == '__main__':
    #log_location()
    #evaluate_all_models()
    predict_current_location()
    #stream_location()