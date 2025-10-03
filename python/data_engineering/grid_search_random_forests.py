# -*- coding: utf-8 -*-
"""
Created on Thu Oct  2 11:28:20 2025

@author: BRD5CLJ
"""
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
  

if __name__ =="__main__":
    
    param_grid = {
    'n_estimators': [50, 100, 150],  
    'max_depth': [None, 10, 20], 
    'min_samples_split': [2, 5, 10],  
    'min_samples_leaf': [1, 2, 4], 
    'max_features': ['sqrt', 'log2', None]
   }
    fh = FileHandler()
    path = fh.select_file()
    
    #read dataset
    dataset = pd.read_csv(path,index_col = 0)
    
    #extract features, labels and columns
    dataset_features,dataset_labels,columns = extract_data_labels(dataset,[])
    
    #train and test 
    X_train,X_test,y_train,y_test = train_test_split(dataset_features, dataset_labels, test_size = 0.2,random_state=41)
    

    # Train Random Forest
    model = RandomForestClassifier(n_estimators=100, random_state=48, class_weight = "balanced")
    
    grid_search = GridSearchCV(estimator=model, 
                           param_grid=param_grid, 
                           cv=5, 
                           n_jobs=-1, 
                           scoring = 'accuracy',
                           verbose =  True)
    
    # Fit GridSearchCV to the training data
    grid_search.fit(X_train, y_train)
    # Get the best model from GridSearchCV and make predictions
    best_rf_model = grid_search.best_estimator_
    y_pred_gs = best_rf_model.predict(X_test)
    y_pred_prob_gs = best_rf_model.predict_proba(X_test)[:, 1]  # For ROC-AUC
    # Calculate accuracy and ROC-AUC for the best model
    accuracy = accuracy_score(y_test, y_pred_gs)
    roc_auc = roc_auc_score(y_test, y_pred_prob_gs)
    # Cross-validation for accuracy and ROC-AUC
    accuracy_scores = grid_search.cv_results_['mean_test_score']
    mean_accuracy = np.mean(accuracy_scores)
    std_accuracy = np.std(accuracy_scores)
    roc_auc_scores = cross_val_score(best_rf_model, X_train, y_train, cv=5, scoring=make_scorer(roc_auc_score))
    mean_roc_auc = np.mean(roc_auc_scores)
    std_roc_auc = np.std(roc_auc_scores)
    # Display results
    print(f"Best Hyperparameters from Grid Search: {grid_search.best_params_}")
    print(f"Cross-validation Accuracy: {mean_accuracy:.4f} ± {std_accuracy:.4f}")
    print(f"Cross-validation ROC-AUC: {mean_roc_auc:.4f} ± {std_roc_auc:.4f}")
    print(f"Test Accuracy: {accuracy:.4f}")
    print(f"Test ROC-AUC: {roc_auc:.4f}")
    
    import json
    with open("random_forest_params.json","w") as f:
        json.dump(grid_search.best_params_, f)