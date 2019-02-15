import pandas as pd
import numpy as nm
import sqlite3
from scipy.sparse.linalg import svds
from sqlalchemy import create_engine
import subprocess,psycopg2
conn_info = subprocess.run(["heroku", "config:get", "DATABASE_URL", "-a", moviesrsfinder], stdout = subprocess.PIPE)
connuri = conn_info.stdout.decode('utf-8').strip()
engine=create_engine(connuri)
raw_engine = engine.raw_connection()

def recommend_movies(predictions_df, userID, movies_df, original_ratings_df, num_recommendations=5):
    user_row_number = userID - 1
    #print(user_row_number)
    sorted_user_predictions = predictions_df.iloc[user_row_number].sort_values(ascending=False)
    user_data = original_ratings_df[original_ratings_df.account_id == (userID)]
    user_full = (user_data.merge(movies_df, how = 'left', left_on = 'movie_id', right_on = 'movie_id').
                     sort_values(['rating'], ascending=False))
    recommendations = (movies_df[~movies_df['movie_id'].isin(user_full['movie_id'])].
         merge(pd.DataFrame(sorted_user_predictions).reset_index(), how = 'left',
               left_on = 'movie_id',
               right_on = 'movie_id').
         rename(columns = {user_row_number: 'Predictions'}).
         sort_values('Predictions', ascending = False).
                       iloc[:num_recommendations, :-1]
                      )
    return recommendations

def calculate(x):
    db=sqlite3.connect('db.sqlite3')
    movies_df = pd.read_sql_query("SELECT * FROM movies",raw_engine)
    ratings_df = pd.read_sql_query("SELECT * FROM rating", raw_engine)
    R_df = ratings_df.pivot(index = 'account_id', columns ='movie_id', values = 'rating').fillna(0)
    R=R_df.values
    user_ratings_mean=nm.mean(R,axis=1)
    R_demeaned = R - user_ratings_mean.reshape(-1, 1)
    U, sigma, Vt = svds(R_demeaned, k = 1)
    sigma = nm.diag(sigma)
    all_user_predicted_ratings = nm.dot(nm.dot(U, sigma), Vt) + user_ratings_mean.reshape(-1, 1)
    preds_df = pd.DataFrame(all_user_predicted_ratings, columns = R_df.columns)
    #print(preds_df)
    predictions = recommend_movies(preds_df, x, movies_df, ratings_df, 15)
    return predictions


