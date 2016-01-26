# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 18:42:31 2015

@author: zhihuixie
"""

import pandas as pd

def ranks(rate_dict):
    """
    input as a dictornary, key as movie id and name, values as calculated 
    parameters of rating
    """
    sorted_dict = sorted(rate_dict, key = lambda x: rate_dict[x], reverse = True)
    return sorted_dict
    
def mean_rate(df):
    """
    input a pandas dataframe, return mean of rate for each movie
    """
    mean_of_rate = dict(df.mean())
    return mean_of_rate
    
def count_rate(df):
    """
    input a pandas dataframe, return number of rate for each movie
    """
    number_of_rate = dict(df.count())
    return number_of_rate

def positive_rate(df): 
    """
    Calculate the percentage of ratings for each movie that are 4 or higher.
    """
    pos_rate_percentages = {}
    movies = df.columns.values
    nrows, ncols = df.shape[0], df.shape[1]
    for i in range(ncols):
        pos_rate = [df.iloc[j, i] for j in range(nrows) if df.iloc[j, i] >= 4]
        pos_rate_percentage = len(pos_rate)*1.0/df.iloc[:, i].count()
        pos_rate_percentages[movies[i]] = pos_rate_percentage
    return pos_rate_percentages
    
def similarity_rate(target_movie, df):
    """
    Use (x&y)/x to compute similarity — that is, 
    compute the probability that the user rated movie i given that they 
    also rated 260: Star Wars: Episode IV - A New Hope (1977).
    """
    nrows, ncols = df.shape[0], df.shape[1] #number of users and movies
    common_rates = {} #define a dictornary for user who rate both target movie and another movie
    movies = df.columns.values #names of movies
    is_not_rate_target = df[target_movie].isnull() #True for rate, False for not rate
    num_of_target_rate = df[target_movie].count()# count number of total rate
    for i in range(ncols):
        is_not_rate = df.iloc[:, i].isnull()#True for rate, False for not rate
        #calculate number of common rate
        common_rate = len([n for n in range(nrows) if not is_not_rate_target[n] \
                       and is_not_rate_target[n] == is_not_rate[n]])
        #calculate the percentage of target raters who also rated that movie
        common_rates[movies[i]] = common_rate * 1.0 / num_of_target_rate
    return common_rates

if __name__ == "__main__":    

    df = pd.read_csv("A1Ratings.csv", usecols = range(1,21))
    #Quiz Part I - mean of rate
    mean_of_rate = ranks(mean_rate(df))
    print "The top5 mean of rate:"
    print mean_of_rate[:5], "\n"

    #Quiz Part II - number of rate
    number_of_rate = ranks(count_rate(df))
    print "The top5 number of rate:"
    print number_of_rate[:5], "\n"
    
    #Quiz Part III - fraction of positive ratings
    pos_rate_percentages = ranks(positive_rate(df))
    print "The top5 positive percentage of rate:"
    print pos_rate_percentages[:5], "\n"
    
    #Quiz Part VI - fraction of positive ratings
    target_movie = "260: Star Wars: Episode IV - A New Hope (1977)"
    common_rates = ranks(similarity_rate(target_movie, df))  
    print "The top5 common_rates:"
    print common_rates[1:6], "\n"      
