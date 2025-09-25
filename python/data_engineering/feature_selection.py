# -*- coding: utf-8 -*-
"""
Created on Tue Sep 23 15:55:29 2025

@author: BRD5CLJ
"""

from utils import FileHandler
import pandas as pd
from sklearn.feature_selection import SelectKBest, f_classif, mutual_info_classif
import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVC, LinearSVC
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline

def plot_bar_graph(feature_scores_dict, feature_list,width):
    
    x = np.arange(len(feature_list))
    multiplier = 0 
    fig = plt.figure(figsize=(20,10))
    ax = fig.gca()
    for attribute, measurement in feature_scores_dict.items():
        offset = width * multiplier 
        rects = ax.bar(x + offset, measurement, width, label = attribute)
        ax.bar_label(rects, padding=6)
        multiplier += 1
        
    
    ax.set_ylabel('Length (mm)')
    ax.set_title('Penguin atributes by species')
    ax.set_xticks(x + width,feature_list, rotation=45)
    ax.legend(loc='upper left', ncols=2)
    plt.show()
    
if __name__ == "__main__":

    #file handler    
    fh = FileHandler()
    path = fh.select_file()
    
    #read dataset
    dataset = pd.read_csv(path,index_col = 0)
    
    #drop 0 columns
    zero_column = [col for col in dataset.columns if (dataset[col] == 0).all()]
    
    #dataset
    dataset = dataset.drop(columns = zero_column,axis=1)
    columns = dataset.columns[:-1]
    
    #datset numpy
    dataset_numpy = dataset.to_numpy()
    
    #dataset_labels
    dataset_labels = dataset_numpy[:,-1]
    
    #dataset_features
    dataset_features = dataset_numpy[:,:-1]
    dataset_features = dataset.iloc[:,:-1]
    
    #number of dataset_features
    N_FEATURES = 5
    
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
    
    scores_dict={}
    scores_dict["ANOVA"] = feature_scores_ANOVA/max(feature_scores_ANOVA)
    scores_dict["MI"] =  feature_scores_MI
    
    plot_bar_graph(scores_dict, columns,width=0.5)
    
    print("Most relevant MI dataset_features: ", selected_feature_names_MI )
    print("Most relevant ANVOVA dataset_features: ",selected_feature_names_ANOVA )


    ##apply a simple lienar classifier
    from sklearn.model_selection import train_test_split
    
    
    X_train, X_test, y_train, y_test = train_test_split(dataset_features, dataset_labels, test_size=0.2, random_state=42)
    model = LinearSVC(loss ="squared_hinge",dual=False, tol=1e-3,verbose=1,max_iter = 100000)
    pipeline = Pipeline([
        ('feature_selection', SelectKBest()),
         ('classifier', model )])
    
    param_grid = {
        'classifier__penalty' : [ "l1"],
        'feature_selection__score_func' : [f_classif,mutual_info_classif],
        'feature_selection__k': [2,5,10,15,20,26],
        'classifier__C' : [1,10,50,100]
        }
    
    grid_search = GridSearchCV(
        estimator = pipeline,
        param_grid = param_grid,
        cv=5,   #5-fold cross-validation
        scoring = 'accuracy',
        n_jobs = -1, #use all available cores
        verbose = 1
        )
    
    #grid search
    grid_search.fit(X_train,y_train)
    best_score = grid_search.best_score_
    best_pipeline = grid_search.best_estimator_
    
    #selected features and params
    
    best_params = grid_search.best_params_ 
    
    #model
    best_model = best_pipeline.named_steps['classifier']
    best_selector = best_pipeline.named_steps['feature_selection']
    best_features = best_selector.get_feature_names_out()
    best_coefs = best_model.coef_.flatten()
    
    acc = best_pipeline.score(X_test, y_test)
    
    weights=[0]*26
    
    i=0
    j=0
    
    while  j < len(best_coefs):
        if columns[i] == best_features[j]:
            weights[i] = abs(best_coefs[j])
            i+=1
            j+=1
    
        else :
            i+=1
        
                
    scores_dict["SVM"] = weights
    scores_dict["SVM"] = scores_dict["SVM"] / max(scores_dict["SVM"])
    
    #bin bars
    plot_bar_graph(scores_dict, columns, width = 0.3)
    