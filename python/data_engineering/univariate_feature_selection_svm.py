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
import os 

def dict_importances(dataset_features,dataset_labels,metric=None,columns=None,score=None,num_features=None):
    
    #dataset_features based on mutual information
    selector_MI = SelectKBest(score_func = mutual_info_classif, k = num_features)
    features_new_MI = selector_MI.fit_transform(dataset_features,dataset_labels)
    feature_names_MI = selector_MI.feature_names_in_
    feature_scores_MI = selector_MI.scores_
    selected_feature_names_MI = selector_MI.get_feature_names_out()
    
    #feature based on ANOVA
    selector_ANOVA = SelectKBest(score_func = f_classif, k = num_features)
    features_new_ANOVA = selector_ANOVA.fit_transform(dataset_features,dataset_labels)
    feature_names_ANOVA = selector_ANOVA.feature_names_in_
    feature_scores_ANOVA = selector_ANOVA.scores_
    selected_feature_names_ANOVA = selector_ANOVA.get_feature_names_out()
    metrics = ["MI","ANOVA"]
    scores = [feature_scores_MI, feature_scores_ANOVA]
    
    if metric != None:
        metrics.append(metric)
        scores.append(score)
    
    #scores dict
    scores_dict = {key_m : { key_s : value for key_s, value in zip(columns,abs(scores[it]/max(scores[it])))} for it,key_m in enumerate(metrics)}
    
    return scores_dict
    
def plot_bar_graph(feature_scores_dict, width):
    n_features = len(next(iter(feature_scores_dict.values())))
    x = np.arange(n_features)
    multiplier = 0 
    fig = plt.figure(figsize=(20,10))
    ax = fig.gca()
    for attribute, score in feature_scores_dict.items():
        offset = width * multiplier 
        rects = ax.bar(x + offset, score.values(), width, label = attribute)
        ax.bar_label(rects, padding=6)
        multiplier += 1
        
    
    ax.set_ylabel('Length (mm)')
    ax.set_title('Penguin atributes by species')
    ax.set_xticks(x + width, score.keys(), rotation=45)
    ax.legend(loc='upper left', ncols=2)
    plt.show()

def save_dataframe_table(dictionary,path):
    dataframe = pd.DataFrame.from_dict(dictionary)
    dataframe = dataframe.drop(columns=['param_feature_selection__score_func','mean_fit_time','mean_fit_time',	'std_fit_time',  'mean_score_time', 'std_score_time','params'])
    dataframe.to_csv(path)

def extract_data_labels(dataset,features_to_remove):
    #drop 0 columns
    zero_columns = [col for col in dataset.columns if (dataset[col] == 0).all()]
    features_to_remove.extend(zero_columns)
    #dataset
    dataset = dataset.drop(columns = features_to_remove,axis=1)
    columns = dataset.columns[:-1]
    
    #datset numpy
    dataset_numpy = dataset.to_numpy()
    
    #dataset_labels
    dataset_labels = dataset_numpy[:,-1]
    
    #dataset_features
    dataset_features = dataset_numpy[:,:-1]
    dataset_features = dataset.iloc[:,:-1]
    
    return dataset_features,dataset_labels,columns
    
if __name__ == "__main__":

    #file handler    
    fh = FileHandler()
    path = fh.select_file()
    
    #read dataset
    dataset = pd.read_csv(path,index_col = 0)
    
    #extract features, labels and columns
    dataset_features,dataset_labels,columns = extract_data_labels(dataset)
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
    
  
    print("Most relevant MI dataset_features: ", selected_feature_names_MI )
    print("Most relevant ANVOVA dataset_features: ",selected_feature_names_ANOVA )


    ##apply a simple lienar classifier
    from sklearn.model_selection import train_test_split
    
    
    X_train, X_test, y_train, y_test = train_test_split(dataset_features, dataset_labels, test_size=0.2, random_state=42)
    model1 = LinearSVC(loss ="squared_hinge",dual=False, tol=1e-3,verbose=1,max_iter = 100000)
    model2 = SVC(gamma = 'scale', tol = 1e-3,verbose=1, max_iter = 100000)
    pipeline = Pipeline([
        ('feature_selection', SelectKBest()),
         ( 'classifier', model2 )])
    
    param_grid1 = {
        'classifier__penalty' : [ "l1","l2"],
        'feature_selection__score_func' : [f_classif,mutual_info_classif],
        'feature_selection__k': np.arange(1,len(columns)),
        'classifier__C' : [1,10,50,100]
        }
    #num_features =list(np.arange(1,len(columns)+1))
    num_features = [1]
    param_grid2 = {
        'feature_selection__score_func' : [f_classif,mutual_info_classif],
        'feature_selection__k': num_features,
        'classifier__C' : [1,10,50,100],
        'classifier__degree' : [3,5,7],
        'classifier__kernel' : ['linear', 'poly', 'rbf','sigmoid']
        }
    
    grid_search = GridSearchCV(
        estimator = pipeline,
        param_grid = param_grid2,
        cv=5,   #5-fold cross-validation
        scoring = 'accuracy',
        n_jobs = -1, #use all available cores
        verbose = 1
        )
    
    #grid search
    grid_search.fit(X_train, y_train)
    
    dictionary = grid_search.cv_results_
    save_dataframe_table(dictionary, os.path.join(os.path.dirname(path[:-4]),"grid_search_table.csv"))
    
    best_score = grid_search.best_score_
    best_pipeline = grid_search.best_estimator_
    
    #selected features and params
    best_params = grid_search.best_params_ 
    
    #model
    best_model = best_pipeline.named_steps['classifier']
    best_selector = best_pipeline.named_steps['feature_selection']
    best_features = best_selector.get_feature_names_out()
    acc = best_pipeline.score(X_test, y_test)
    scores =[]
    
    scores.append(feature_scores_ANOVA)
    scores.append(feature_scores_MI)
    
    metrics = [ "ANOVA","MI"] 
    scores_dict = dict_importances(metrics, columns, scores)
    plot_bar_graph(scores_dict, width = 0.5)
    
    if hasattr(best_model, 'coef_'):
        best_coefs = best_model.coef_.flatten()
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
                
        metrics = [ "ANOVA","MI","SVM"] 
        
        scores_dict["SVM"] =  dict(zip(columns,weights/max(weights)))
        
        #bin bars
        plot_bar_graph(scores_dict, columns, width = 0.3)
    