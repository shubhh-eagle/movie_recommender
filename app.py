import pickle
import streamlit as st

#for hashing password 
import hashlib

#import database management functions
from manage_db import *

# Generating hash for password
def generate_hashes(password):

    #sha 256bit algorithm for password hash encoding , getting hex digest(coded segment)
	return hashlib.sha256(str.encode(password)).hexdigest()

# Verify hash of inputted password with the corresponding user's password's hash saved in database
def verify_hashes(password,hashed_text):
	if generate_hashes(password) == hashed_text:
		return hashed_text
	return False

# Unpickling model and final rating matrix
model = pickle.load(open('model.pkl','rb'))
final_rating = pickle.load(open('final_rating.pkl','rb'))

# Concerting to pivot matrix
movie_pivot = final_rating.pivot_table(index='title',columns='userId',values='rating').fillna(0)

# Function to get recommendations
def recommend(query_movie):
    
    distances, indices = model.kneighbors(movie_pivot.loc[query_movie,:].values.reshape(1, -1), n_neighbors = 6)
    rec_movies = []

    for i in range(1, len(distances.flatten())):
        rec_movies.append(movie_pivot.index[indices.flatten()[i]])
    return rec_movies


st.title("Movie Recommender App")

menu = ['Home' , 'Login' , 'Signup']

choice = st.sidebar.selectbox("Menu",menu)

if choice == "Login":
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password",type='password')
    if st.sidebar.checkbox("Login"):
        create_usertable()
        hashed_pswd = generate_hashes(password)
        result = login_user(username,verify_hashes(password,hashed_pswd))
        if result:
            st.success("Welcome {}".format(username))

            st.subheader('Movie Recommender System')
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

    else:
        st.warning("Incorrect Username/Password")

elif choice == "SignUp":
    new_username = st.text_input("User name")
    new_password = st.text_input("Password", type='password')

    confirm_password = st.text_input("Confirm Password",type='password')
    if new_password == confirm_password:
        st.success("Password Confirmed")
    else:
        st.warning("Passwords not the same")

    if st.button("Submit"):
        create_usertable()
        hashed_new_password = generate_hashes(new_password)
        add_userdata(new_username,hashed_new_password)
        st.success("You have successfully created a new account")
        st.info("Login to Get Started")

else:
    st.subheader("Home")


