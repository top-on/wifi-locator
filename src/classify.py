# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 07:15:05 2017

@author: DETJENS2
"""

from sklearn.metrics import confusion_matrix
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
import numpy as np

from windows import get_feature_matrix
from windows import get_labels



def evaluate_model(model, x, y):
    model.fit(x, y.values.ravel())
    y_pred = model.predict(x)
    labels = list(set(y.values.ravel()))
    print('Random Forests:')
    print('Labels: %s' % labels)
    print('Confusion_matrix (reusing data):')
    print(confusion_matrix(y.values.ravel(), y_pred, labels=labels))
    print('CV f1_micro (not reusing data): %s' 
          % np.mean(cross_val_score(model, x, y.values.ravel(), cv=5, scoring='f1_micro')))


x = get_feature_matrix()
y = get_labels()
#print(x)
#print(y)

# KNN
model = KNeighborsClassifier(n_neighbors=3, algorithm='auto', metric='braycurtis') 
evaluate_model(model, x, y)

# decision trees
model = RandomForestClassifier(n_estimators=50)
evaluate_model(model, x, y)
    
    
    
