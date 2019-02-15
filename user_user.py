import pandas as pd
import numpy as np
import sqlite3
from sqlalchemy import create_engine
import subprocess
proc = subprocess.Popen('heroku config:get DATABASE_URL -a moviesrsfinder', stdout=subprocess.PIPE, shell=True)
db_url = proc.stdout.read().decode('utf-8').strip()
engine = create_engine(db_url)


def calculateuser(x):
    db=sqlite3.connect('db.sqlite3')
    movies = pd.read_sql_query("SELECT * FROM movies", con=engine)
    ratings = pd.read_sql_query("SELECT * FROM rating", con=engine)
            
    userRatings=ratings.pivot_table(index=['movie_id'], columns=['account_id'], values='rating')
    corrMatrix=userRatings.corr(method='pearson')
    #print (corrMatrix)       
    myUsers=corrMatrix.loc[x].dropna()
    #print(x)
    myUsers.sort_values(inplace=True,ascending=False)
    #print (myUsers)
    userRatings=ratings.pivot_table(index=['account_id'], columns=['movie_id'], values='rating')
    simCandidates=pd.Series()
    for i in range (1,min(6,len(myUsers.index))):
        myRatings=userRatings.loc[myUsers.index[i]].dropna()
        myRatings.sort_values(inplace=True,ascending=False)
        #print(myRatings.iloc[10:])
        for j in range(0,10):
            #print(myRatings.iloc[[j]])
            simCandidates=simCandidates.append(myRatings.iloc[[j]])


    
    simCandidates.sort_values(inplace=True,ascending=False)
    simCandidates = simCandidates[~simCandidates.index.duplicated(keep='first')]
    myRatings=userRatings.loc[x].dropna()
    for i in range(0,len(myRatings.index)):
        for j in range(0,len(simCandidates.index)):
            if(simCandidates.index[j]==myRatings.index[i]):
                simCandidates=simCandidates.drop(labels=simCandidates.index[j],axis=0)
                break
    #print(simCandidates)
    #print(myRatings)
    return simCandidates