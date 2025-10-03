# -*- coding: utf-8 -*-
"""
Created on Mon Sep 29 13:59:25 2025

@author: BRD5CLJ
"""


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
from univariate_feature_selection_svm import dict_importances

if __name__ == "__main__": 
    fh = FileHandler()
    path = fh.select_file()
    
    #read dataset
    dataset = pd.read_csv(path,index_col = 0)
    
    #extract features, labels and columns
    dataset_features,dataset_labels,columns = extract_data_labels(dataset)
    X_train, X_test, y_train, y_test = train_test_split(dataset_features,dataset_labels)
    
    # Create pipeline with RFE
    model = LogisticRegression(max_iter=1000, solver='liblinear',penalty='l1',C=1) 
    
    #Fit the RFECV
    model.fit(X_train, y_train)
    # Get feature importances from the fitted estimator
    importances = model.coef_
    
    score = model.score(X_test,y_test)
    
    N_FEATURES = 6
    #dataset_features based on mutual information
    selector_MI = SelectKBest(score_func = mutual_info_classif, k = N_FEATURES)
    features_new_MI = selector_MI.fit_transform(dataset_features,dataset_labels)
    feature_names_MI = selector_MI.feature_names_in_
    feature_scores_MI = selector_MI.scores_
    selected_feature_names_MI = selector_MI.get_feature_names_out()
    
    #feature based on ANOVA
    selector_ANOVA = SelectKBest(score_func = f_classif, k = N_FEATURES)
    features_new_ANOVA = selector_ANOVA.fit_transform(dataset_features,dataset_labels)
    feature_names_ANOVA = selector_ANOVA.feature_names_in_
    feature_scores_ANOVA = selector_ANOVA.scores_
    selected_feature_names_ANOVA = selector_ANOVA.get_feature_names_out()
    
    scores =[]
    scores.append(feature_scores_ANOVA)
    scores.append(feature_scores_MI)
    scores.append(importances.flatten())
    metrics = ["ANOVA","MI","Model"]    
    scores_dict = dict_importances(metrics,columns,scores,10)
    plot_bar_graph(scores_dict, width = 0.3)