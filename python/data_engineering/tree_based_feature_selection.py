# -*- coding: utf-8 -*-
"""
Created on Tue Sep 30 14:26:01 2025

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
from sklearn.decomposition import PCA,KernelPCA
import json


# Helper function to perform cross-validation
def evaluate_with_cv(X_selected, y, model, method_name,cv=5):
   
    scores = cross_val_score(model, X_selected, y, cv = cv, scoring='accuracy')
    print(f'Cross-validated accuracy ({method_name}): {np.mean(scores):.2f} ± {np.std(scores):.2f}')


if __name__ == "__main__": 
  
    
    
    fh = FileHandler()
    path = fh.select_file()
    
    #read dataset
    dataset = pd.read_csv(path,index_col = 0)
    
    #extract features, labels and columns
    dataset_features,dataset_labels,columns = extract_data_labels(dataset,[])
    
   
    #train and test 
    X_train,X_test,y_train,y_test = train_test_split(dataset_features, dataset_labels, test_size = 0.2,random_state=45)
    
    with open("random_forest_params.json","r") as f:
        loaded_params = json.load(f)
        
    #Random Forests
    model = RandomForestClassifier(**loaded_params)
    model.fit(X_train,y_train)
    
    corr_matrix_data = corr_matrix(dataset,"Dataset Corr matrix")
    display_mi_matrix(dataset,"Dataset Mutual Information matrix")
    score = model.score(X_test,y_test)
    print(f"Test score: {score}")
    
    # Get feature importances
    importances = model.feature_importances_
    feature_names = columns
    dict_scores = dict_importances(dataset_features,dataset_labels,"Random Forest",columns,importances,10)
    data_frame_dict = pd.DataFrame.from_dict(dict_scores)
    data_frame_dict["CORR"] = corr_matrix_data["label"][:-1]
    
    #Custom 
    top_custom_features = ['peak_heights 1' ,'widths 1' ,'widths 2','prominences 1','prominences 2','skewness','peak entropy']
    NUM_FEATURES = len(top_custom_features)
    #PCA
    pca = PCA(n_components = NUM_FEATURES)
    kernel_pca = KernelPCA(
    n_components=None, kernel="poly", gamma=10, fit_inverse_transform=True, alpha=0.1
    )   
    pca.fit(dataset_features)
    dataset_transformed1 = pca.transform(dataset_features)
    kernel_pca.fit(dataset_features)
    dataset_transformed2 = pca.transform(dataset_features)
    
    #RF
    top_RF = data_frame_dict['Random Forest'].sort_values(ascending=False)[:NUM_FEATURES]
    top_RF_scores = top_RF.values
    top_RF_features = top_RF.index.values
    
    #ANOVA
    top_ANOVA = data_frame_dict['ANOVA'].sort_values(ascending=False)[:NUM_FEATURES]
    top_ANOVA_scores = top_ANOVA.values
    top_ANOVA_features = top_ANOVA.index.values
    
    #MI
    top_MI = data_frame_dict["MI"].sort_values(ascending=False)[:NUM_FEATURES]
    top_MI_scores = top_MI.values
    top_MI_features = top_MI.index.values
    
    #Corrrelation
    top_CORR= data_frame_dict["MI"].sort_values(ascending=False)[:NUM_FEATURES]
    top_CORR_scores = top_CORR.values
    top_CORR_features = top_CORR.index.values
    
    cumulated_metric = data_frame_dict.sum(axis=1)
    top_cumulated = cumulated_metric.sort_values(ascending=False)[:NUM_FEATURES]
    top_cumulated_scores = top_cumulated.values
    top_cumulated_features = top_cumulated.index.values
    
    print(f"RF best {NUM_FEATURES} features: \n",top_RF)
    print()
    print(f"ANOVA best {NUM_FEATURES} features: \n",top_ANOVA)
    print()
    print(f"MI best {NUM_FEATURES} features: \n",top_MI)
    print()
    print(f"Corr best {NUM_FEATURES} features: \n",top_CORR)
    print()
    print(f"Cumulated best {NUM_FEATURES} features: \n",top_cumulated)
    
    plot_bar_graph(dict_scores, width = 0.3)
    
    model = RandomForestClassifier(**loaded_params)
    print()
    cv=10
    # Evaluate each feature selection method
    X_selected = dataset_features[top_RF_features]
    evaluate_with_cv(X_selected, dataset_labels, model, 'RF',cv)
    X_selected = dataset_features[top_ANOVA_features]
    evaluate_with_cv(X_selected, dataset_labels, model, 'ANOVA',cv)
    X_selected = dataset_features[top_MI_features]
    evaluate_with_cv(X_selected, dataset_labels, model, 'MI',cv)
    X_selected = dataset_features[top_CORR_features]
    evaluate_with_cv(X_selected, dataset_labels, model, 'CORR',cv)
    X_selected = dataset_features[top_custom_features]
    evaluate_with_cv(X_selected, dataset_labels, model, 'custom',cv)
    X_selected = dataset_features[top_cumulated_features]
    evaluate_with_cv(X_selected, dataset_labels, model, 'cumulated',cv)
    evaluate_with_cv(dataset_transformed1, dataset_labels, model,'PCA',cv)
    evaluate_with_cv(dataset_transformed2, dataset_labels, model,'K_PCA',cv)