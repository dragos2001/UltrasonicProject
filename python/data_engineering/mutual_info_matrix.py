# -*- coding: utf-8 -*-
"""
Created on Thu Sep 25 13:20:09 2025

@author: BRD5CLJ
"""
import numpy as np
import pandas as pd
from utils import FileHandler
import seaborn as sns
import matplotlib.pyplot as plt

def compute_entropy(histogram):
    entropy =-np.sum(histogram*(np.log2(histogram)))
    return entropy
            
def display_mi_matrix(dataset,title = "Mutual info matrix", nbins=None):
    mi_info_matrix, entropy_matrix, probs_matrix = mutual_info_matrix(dataset, nbins)
    columns = dataset.columns
    plt.figure(figsize=(20,14))
    ax = sns.heatmap(mi_info_matrix,annot=True, fmt=".2f", xticklabels = columns, yticklabels = columns)
    plt.title(title)
    
def mutual_info_matrix(dataset, nbins=None):
    
   
    #features
    features = dataset.columns.values
    N = len(features)
    
    #nbins
    if nbins == None:
        nbins = int(np.sqrt(len(dataset)))
        
    #histogram matrix
    histogram_matrix = np.zeros(( N, N, nbins, nbins))
    probs_matrix = np.zeros(( N, N, nbins, nbins))
    entropy_matrix = np.zeros((N,N))
    for it1,feature1 in enumerate(features):
        for it2,feature2 in enumerate(features):
                X = dataset[feature1]
                Y = dataset[feature2]
                histogram_matrix[it1,it2,:,:],_ ,_ = np.histogram2d(X, Y, bins = nbins)
                probs_matrix[it1,it2] = histogram_matrix[it1,it2] / len(dataset) + 1e-100
                entropy_matrix[it1,it2] = compute_entropy(probs_matrix[it1,it2])
  
    #single entropies
    single_entropies = entropy_matrix.diagonal()
    H = np.tile(single_entropies,(N,1) )
    Ht = H.T
    mi_matrix = H + Ht - entropy_matrix
    norm_mi_matrix = mi_matrix * 2 / (H + Ht)
    
    return norm_mi_matrix,entropy_matrix,probs_matrix
   
   




if __name__ == "__main__":
    
    fh = FileHandler()
    path = fh.select_file()
    dataset = pd.read_csv(path, index_col = 0)
    display_mi_matrix(dataset, title = "Mutual Info Matrix", nbins=None)