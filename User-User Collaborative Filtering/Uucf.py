# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 19:41:27 2015

@author: zhihuixie
"""

import pandas as pd
import numpy as np

class UCF():
    """
    define user-user based recommendation system
    """
    def __init__(self, df):
        """
        one parameter: pandas data frame
        """
        self.df = df
        self.data = np.array(df.values)
        self.rows = df.index.values
        
    def p_corr(self):
        """
        calculate pearson correlation between users
        """
        data = self.data
        rows = self.rows
        (nrows, ncols) = data.shape
        p_corr_dict = {}

        for row_i in range(nrows):
            for row_j in range(nrows):
                valide_data_i = [data[row_i, :][n] \
                            for n in range(ncols) if \
                            data[row_i, n] != 0 and data[row_j, n] != 0]
                valide_data_j = [data[row_j, :][n] \
                                for n in range(ncols) if \
                                data[row_i, n] != 0 and data[row_j, n] != 0] 
                valide_data_i = np.array(valide_data_i) - np.mean(valide_data_i)
                valide_data_j = np.array(valide_data_j) - np.mean(valide_data_j)
                #print np.dot(data[row_i, :], data[row_j, :])
                p_corr = np.dot(valide_data_i, valide_data_j)*1.0/\
                         np.sqrt(sum(np.power(valide_data_i,2))*\
                                 sum(np.power(valide_data_j,2)))
                p_corr_dict[(rows[row_i], rows[row_j])] = p_corr  
        return p_corr_dict
        
    def p_corr_rank(self, user_id, n):
        """
        rank correlations between users and choose top n correlated users
        """
        p_corrs = self.p_corr()
        p_corrs_row = {}
        ranked_p_corrs = {}
        for (a, b) in p_corrs:
            if user_id == a:
                p_corrs_row[(a, b)] = p_corrs[(a, b)] 
        sorted_p_corrs = sorted(p_corrs_row, reverse = True, \
                         key = lambda x: p_corrs_row[x])[1:n + 1]
        for (i, j) in sorted_p_corrs:
            ranked_p_corrs[(i, j)] = p_corrs_row[(i, j)] 
        return ranked_p_corrs
        
    def prediction (self, user_id, n):
        """
        predict score without normalization
        """
        ranked_p_corrs = self.p_corr_rank(user_id, n)
        neighbors = [b for (a, b) in ranked_p_corrs.keys()]
        weights = ranked_p_corrs.values()
        df = self.df
        preds = []
        for col in df.columns:
            values = 0
            weights = 0
            for neighbor in neighbors:
                value = df.loc[neighbor, col]
                if value == 0:
                    weight = 0
                else:
                    weight = ranked_p_corrs[(user_id, neighbor)]
                values += value*weight
                weights += weight
            if weights == 0:
                preds.append(0)
            else:
                preds.append(values*1.0/weights)
        return preds
        
    def prediction_with_nor(self, user_id, n):
        """
        predict score with normalization
        """
        ranked_p_corrs = self.p_corr_rank(user_id, n)
        neighbors = [b for (a, b) in ranked_p_corrs.keys()]
        weights = ranked_p_corrs.values()
        df = self.df
        preds = []
        user_mean = np.mean([num for num in df.loc[user_id, :] if num != 0 ])
        n_mean = {}
        for neighbor in neighbors:
            n_mean[neighbor] = np.mean([num for num in df.loc[neighbor, :] \
                                       if num != 0 ]) 
        for col in df.columns:
            values = 0
            weights = 0
            for neighbor in neighbors:
                value = df.loc[neighbor, col]
                if value == 0:
                    weight = 0
                else:
                    weight = ranked_p_corrs[(user_id, neighbor)]
                values += (value - n_mean[neighbor])*weight
                weights += weight
            if weights == 0:
                preds.append(user_mean)
            else:
                preds.append(user_mean + values*1.0/weights)
        return preds 
    
    def recom(self, user_id, n, m, nor = False):
        """
        recommend top n items
        """
        cols = self.df.columns.values
        if not nor:
            pred = self.prediction(user_id, n)
        else:
            pred = self.prediction_with_nor(user_id, n)
        pred_dict = {}
        for i in range(len(cols)):
            pred_dict[cols[i]] = pred[i]
        top_items = sorted(pred_dict, key = lambda x: pred_dict[x], reverse = True)[:m]
        print "Top 3 movies \t", "\t Prediction"
        for item in top_items:
            print item, "%.3f"%pred_dict[item]
        
        
if __name__ == "__main__":
    df = pd.read_excel("Assignment 3.xls", sheetname = 1)
    df = df.fillna(0)
    ucf = UCF(df)
    #print ucf.p_corr_rank(3712, 5)
    #Q1-12: without normalization
    #Q1-6: user 3867
    print "Top movies for 3867"
    ucf.recom(3867, 5, 3)
    print "\n"
    #Q7-12: user 89
    print "Top movies for 89"
    ucf.recom(89, 5, 3)
    print "\n"
    #Q13-24: with normalization
    #Q13-18: user 3867
    print "Top movies for 3867 with normalization"
    ucf.recom(3867, 5, 3, nor = True)
    print "\n"
    #Q19-24: user 89
    print "Top movies for 89 with normalization"
    ucf.recom(89, 5, 3, nor = True)
    print "\n"
    
         