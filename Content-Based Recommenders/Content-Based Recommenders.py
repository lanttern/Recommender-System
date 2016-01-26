# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 21:41:05 2015

@author: zhihuixie
"""

import pandas as pd
import numpy as np

class CBR():
    """
    This class define a content based recommendation system
    """
    def __init__(self, user_rate, doc_count):
        """
        define 4 parameters which are pandas Series:
        1- user_rate: rating score for a user;
        2- doc_count:key words counting for each document
        3- user_id: id for each user
        4- doc_id: id for each documnent
        """
        self.user_rate = user_rate
        self.doc_count = doc_count
        self.user_id = user_rate.shape[1]
        self.doc_id = doc_count.shape[1]
        
    def user_vector(self, doc_vec):
        """
        generate user rating score for each key word
        """
        user_vec = []
        for i in range(self.user_id):
            user_vec.append([float(np.dot([self.user_rate[:,i]], doc_vec[:,j])) for \
                            j in range(self.doc_id)])
        return user_vec
        
    def doc_vector(self):
        """
        normalizing counting for each key word
        """
        num_attr = np.sum(self.doc_count, axis = 1)
        doc_vec = []
        for i in range(num_attr.shape[0]):
            doc_vec.append(np.sqrt(self.doc_count[i, :]*1.0/num_attr[i]))
        return np.array(doc_vec)
            
    def attr_weight(self):
        """
        calculate weight for each document
        """
        num_doc = np.sum(self.doc_count, axis = 0)
        attr_weights = []
        for i in range(num_doc.shape[0]):
            attr_weights.append(self.doc_count[:,i]*1.0/num_doc[i])
            #attr_weights.append(self.doc_count[:,i]*1.0/math.log(num_doc[i]))
        return np.array(attr_weights)
        
    def naive_predict(self):
        """
        predict rating score without weighting
        """
        user_vec = self.user_vector(self.doc_count)
        preds = []
        for i in range(self.doc_count.shape[0]):
            preds.append([float(np.dot(user_vec[j], self.doc_count[i,:])) for \
                            j in range(self.user_id)])
        return preds
    
    def unit_weight_predict(self, doc_vec = None):
        """
        predict rating score with weighting
        """
        if doc_vec == None:
            doc_vec = self.doc_vector()
        user_vec = self.user_vector(doc_vec)
        preds = []
        for i in range(doc_vec.shape[0]):
            preds.append([float(np.dot(user_vec[j], doc_vec[i,:])) for \
                            j in range(self.user_id)])
        return preds
    
    def idf_weight_predict(self):
        """
        predict rating score with inversed vectorization and weighting
        """
        doc_vec = self.doc_vector()
        attr_weights = self.attr_weight()
        weighted_doc = []
        for i in range(doc_vec.shape[0]):
            weighted_doc.append([np.dot(doc_vec[i,:], attr_weights[:,j]) \
                                for j in range(attr_weights.shape[0])])
        preds = self.unit_weight_predict(doc_vec = np.array(weighted_doc))
        return preds
        
    
if __name__ == "__main__":
    """
    """
    df = pd.read_excel("Assignment 2_clean data.xls")
    df = df.fillna(0, axis = 1)
    doc_count = np.array(df.iloc[:, :10])
    user_rate = np.array(df.iloc[:, 10:])
    
    recommender = CBR(user_rate, doc_count)
    # part 1
    preds1 = np.array(recommender.naive_predict())
    print "Q1: Which document does the simple profile predict user 1 will like best?"
    print [i+1 for i in range(preds1.shape[0]) if preds1[i,0] == max(preds1[:,0])]
    print "Q2: What score does that prediction get?"
    print max(preds1[:,0])
    print "Q3:How many documents does the model predict U2 will dislike \
          (prediction score that is negative)?"  
    print len([i for i in preds1[:,1] if i <0])
    
    #part2
    preds2 = np.array(recommender.unit_weight_predict())
    print "Q4: Which document is now in second with this new model?"
    print "Q5: What prediction score does it have?"
    print preds2[:,0]
    
    #part3
    preds3 = np.array(recommender.idf_weight_predict())
    print "Q6: Compare doc1 and doc9 for user1. What’s user1’s prediction for\
          doc9 in the new IDF weighted model?"
    print preds3[8, 0] #should be 0.179067194 based on excel calculation
    
    
    