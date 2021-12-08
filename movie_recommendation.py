# -*- coding: utf-8 -*-

import pandas as pd
import pickle

movie_path = 'C:/Users/Dell/Downloads/project_1/movies.csv'
rating_path = 'C:/Users/Dell/Downloads/project_1/ratings.csv'

movies_df = pd.read_csv(movie_path,usecols=['movieId','title'],dtype={'movieId': 'int32', 'title': 'str'})
rating_df=pd.read_csv(rating_path,usecols=['userId', 'movieId', 'rating'],dtype={'userId': 'int32', 'movieId': 'int32', 'rating': 'float32'})

movies_df.head()

rating_df.head()

movies_df.info()

rating_df.info()

df = pd.merge(rating_df,movies_df,on='movieId')

combine_movie_rating = df.dropna(axis = 0, subset = ['title'])
combine_movie_rating.head()

movie_ratingCount = (combine_movie_rating.
     groupby(by = ['title'])['rating'].
     count().
     reset_index().
     rename(columns = {'rating': 'totalRatingCount'})
     [['title', 'totalRatingCount']]
    )
movie_ratingCount

rating_with_totalRatingCount = combine_movie_rating.merge(movie_ratingCount, left_on = 'title', right_on = 'title', how = 'left')
rating_with_totalRatingCount.head()

popularity_threshold = 50
rating_popular_movie= rating_with_totalRatingCount.query('totalRatingCount >= @popularity_threshold')
rating_popular_movie.head()

rating_popular_movie.isnull()
rating_popular_movie.isnull().sum().sum()

movie_features_df=rating_popular_movie.pivot_table(index='title',columns='userId',values='rating').fillna(0)
movie_features_df.head()

from scipy.sparse import csr_matrix

movie_features_df_matrix = csr_matrix(movie_features_df.values)

from sklearn.neighbors import NearestNeighbors


model_knn = NearestNeighbors(metric = 'cosine', algorithm = 'brute')
model_knn.fit(movie_features_df_matrix)

query_movie = input("Movie watching right now: ")

distances, indices = model_knn.kneighbors(movie_features_df.loc[query_movie,:].values.reshape(1, -1), n_neighbors = 6)

for i in range(0, len(distances.flatten())):
    if i == 0:
        print('Recommendations for {0}:\n'.format(movie_features_df.index[indices.flatten()[i]]))
    else:
        print('{0}: {1}'.format(i, movie_features_df.index[indices.flatten()[i]]))



pickle.dump(rating_popular_movie,open('C:/Users/Dell/Downloads/project_1/final_rating.pkl','wb'))

pickle.dump(model_knn,open('C:/Users/Dell/Downloads/project_1/model.pkl','wb'))