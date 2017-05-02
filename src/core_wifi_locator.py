"""
Core module of wifi-locator.

Views and APIs need to only import this module.
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
    x = get_feature_matrix()
    y = get_labels()
    # evaluate models
    for name in classifiers.keys():
        evaluate_model(name, classifiers[name], x, y)
    evaluate_model('VotingClassifier', vc, x, y)


def predict_current_location():
    """Predict location label for current wifi signals."""
    # read from sensors
    signals = get_signals()
    # read from model
    x_train = get_feature_matrix()
    y_train = get_labels()
    x_signal = get_signal_matrix(x_train, signals)
    # classify signal
    location = predict(x_train, y_train, x_signal)
    return location


def stream_location():
    """Continuously predict current location."""
    while True:
        print('PreLocation: %s \n' % predict_current_location())
        time.sleep(3)


def log_location(location):
    """Ask for location and log it, together with current wifi signals."""
    # read from sensors
    signals = get_signals()
    # treat case where not enough signals found
    if signals.empty:
        print('Not enough signals!')
        return
    # log location to model
    log_signals(signals, location=location)


# if __name__ == '__main__':
    # log_location()
    # evaluate_all_models()
    # predict_current_location()
    # stream_location()
