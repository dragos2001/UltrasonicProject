# -*- coding: utf-8 -*-
"""
Created on Fri Oct  3 12:37:33 2025

@author: BRD5CLJ
"""

from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import RFECV
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC, LinearSVC
from sklearn.linear_model import SGDClassifier
from utils import FileHandler
import pandas as pd
from univariate_feature_selection_svm import extract_data_labels, plot_bar_graph
import numpy as np
from sklearn.feature_selection import SelectKBest, f_classif, mutual_info_classif
from univariate_feature_selection_svm import dict_importances, plot_bar_graph
from envelope_feature_extraction import corr_matrix
from mutual_info_matrix import display_mi_matrix
from sklearn.model_selection import cross_val_score
from sklearn.metrics import roc_auc_score, make_scorer
import json

fh = FileHandler()
path = fh.select_file()

#read dataset
dataset = pd.read_csv(path,index_col = 0)

#extract features, labels and columns
dataset_features,dataset_labels,columns = extract_data_labels(dataset,[])

#train and test 
X_train,X_test,y_train,y_test = train_test_split(dataset_features, dataset_labels, test_size = 0.2,random_state=41)
top_custom_features = ["distance","left_bases 2","right_bases 2", "peak entropy","skewness","max amp","angle"]
  
    
# Create and train the model
clf = DecisionTreeClassifier()
clf.fit(X_train[top_custom_features], y_train)

score = clf.score(X_test[top_custom_features],y_test)