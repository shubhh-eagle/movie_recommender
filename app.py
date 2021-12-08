import pickle
import streamlit as st

model = pickle.load(open('model.pkl','rb'))
final_rating = pickle.load(open('final_rating.pkl','rb'))
movie_pivot = final_rating.pivot_table(index='title',columns='userId',values='rating').fillna(0)

def recommend(query_movie):
    
    distances, indices = model.kneighbors(movie_pivot.loc[query_movie,:].values.reshape(1, -1), n_neighbors = 6)
    rec_books = []

    for i in range(1, len(distances.flatten())):
        rec_books.append(movie_pivot.index[indices.flatten()[i]])
    return rec_books

st.header('Movie Recommender System')
movie_list=movie_pivot.index.tolist()
query_movie = st.selectbox('Type or Select a Movie from the dropdown',movie_list)

if st.button('Show Recommendation'):
    recommended_movie_names = recommend(query_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
    with col2:
        st.text(recommended_movie_names[1])
    with col3:
        st.text(recommended_movie_names[2])
    with col4:
        st.text(recommended_movie_names[3])
    with col5:
        st.text(recommended_movie_names[4])