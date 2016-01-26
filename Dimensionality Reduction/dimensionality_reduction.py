# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 21:55:28 2016

@author: zhihuixie
"""
import pandas as pd
import numpy as np

class Dim_reduct():
    """
    define dimensionality reduction class
    """
    def __init__(self, u, w, v):
        """
        u: user weight
        w: Singular value
        v:item weight
        """
        self.u = u
        self.w = w
        self.v = v
        
    def feature_score_matrix(self):
        """
        calculate feature score matrix
        """
        return np.dot(self.v,self.w)
    def movie_score_matrix(self):
        """
        calculate movie score matrix
        """
        return np.dot(np.dot(self.u,self.w),(self.v.T))
        
    def matrix_index(self, names):
        """
        mapping matrix id and movie names or user names
        """
        return dict([(b,a) for (a, b) in list(enumerate(names))])    
    
    def recom(self, matrix, user, index_dict, names, n):
        """
        recommend top n items
        """
        index = index_dict[user]
        print "The index for this feature or user:", index
        scores = matrix[:,index]
        scores_dict = dict(zip(names, scores))
        top_items = sorted(scores_dict, key = lambda x: scores_dict[x], \
                           reverse = True)[:n]
        print "The top %d"%n, "items for feature or user", user, "are:"
        print top_items, "\n"

if __name__ == "__main__":
    #load data
    df_u = pd.read_excel("Assignment 6.xlsx",sheetname = 1)
    df_v = pd.read_excel("Assignment 6.xlsx",sheetname = 0)
    df_w = pd.read_excel("Assignment 6.xlsx",sheetname = 2)
    u = np.array(df_u.iloc[:,1:])
    v = np.array(df_v.iloc[:,2:])
    w = np.diagflat(df_w.values)
    #check dim of data
    print u.shape, w.shape, v.shape
    #mapping names
    feature_names = df_u.columns.values[1:]
    user_names = list(df_u.User.values)
    movies_ids = list(df_v["Movie ID"].values)
    #Quize 1 and 2
    dim = Dim_reduct(u, w, v)
    feature_scores = dim.feature_score_matrix()
    feature = 2
    index_dict = dim.matrix_index(feature_names)
    names = movies_ids
    dim.recom(feature_scores, feature, index_dict, names, n = 5)
    
    #Quiz 3
    movie_scores = dim.movie_score_matrix()
    user = 4469
    index_dict = dim.matrix_index(user_names)
    names = movies_ids
    dim.recom(movie_scores.T, user, index_dict, names, n = 5)
