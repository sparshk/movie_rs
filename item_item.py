import pandas as pd
import numpy as np
import sqlite3
from sqlalchemy import create_engine
import subprocess
proc = subprocess.Popen('heroku config:get DATABASE_URL -a moviesrsfinder', stdout=subprocess.PIPE, shell=True)
db_url = proc.stdout.read().decode('utf-8').strip()
engine = create_engine(db_url)

def calculateitem(x):
    db=sqlite3.connect('db.sqlite3')
    movies = pd.read_sql_query("SELECT * FROM movies", con=engine)
    ratings = pd.read_sql_query("SELECT * FROM rating", con=engine)
            
    userRatings=ratings.pivot_table(index=['account_id'], columns=['movie_id'], values='rating')
    corrMatrix=userRatings.corr(method='pearson')       
    myRatings=userRatings.loc[x].dropna()
    simCandidates=pd.Series()
    for i in range (0,len(myRatings.index)):
            sims=corrMatrix[myRatings.index[i]].dropna()
            sims=sims.map(lambda x: x*myRatings[myRatings.index[i]])
            simCandidates=simCandidates.append(sims)
    simCandidates=simCandidates.groupby(simCandidates.index).sum()
    simCandidates.sort_values(inplace=True,ascending=False)
    #print(simCandidates)
    for i in range(0,len(myRatings.index)):
        for j in range(0,len(simCandidates.index)):
            if(simCandidates.index[j]==myRatings.index[i]):
                simCandidates=simCandidates.drop(labels=simCandidates.index[j],axis=0)
                break

    #print(simCandidates)
    #print(myRatings)
    return simCandidates