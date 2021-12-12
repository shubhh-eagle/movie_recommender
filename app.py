import pickle
import pandas as pd
import streamlit as st

#for hashing password 
import hashlib

#import database management functions
from manage_db import *

html_temp = '''
    
    ## To Get Started

    #### 1. Click on the arrow on the top left corner

    #### 2. Click on drop-down menu

    #### 3. If you are new user, then click on Sign-Up Option

    #### 4. If you are existing user, then click on Login Option
'''

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

menu = ['Home' , 'Login' , 'Sign-Up']

choice = st.sidebar.selectbox("Menu",menu)

if choice == "Login":
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password",type='password')

    #using checbox instead of button lets us stay login while doing performing other functions
    if st.sidebar.checkbox("Login"):
        create_usertable()
        hashed_pswd = generate_hashes(password)
        result = login_user(username,verify_hashes(password,hashed_pswd))
        if result:
            st.success("Welcome {}".format(username))

            movie_list=movie_pivot.index.tolist()
            query_movie = st.selectbox('Type or Select a Movie from the dropdown',movie_list)
        
            if st.button('Show Recommendation'):
                recommended_movie_names = recommend(query_movie)

                df = pd.DataFrame(recommended_movie_names, index = [1,2,3,4,5],columns = ['Movie Names'])
                with st.expander("List of Recommended Movies",expanded = True):
                    st.dataframe(df)
               

        else:
            st.warning("Incorrect Username/Password")
    else:
        st.info("Enter Username and Password")
        st.info("Click on the checkbox to Login")

elif choice == "Sign-Up":
    new_username = st.text_input("User name")
    new_password = st.text_input("Password", type='password')

    confirm_password = st.text_input("Confirm Password",type='password')
    if new_password == "" or confirm_password == "":
        pass
    elif new_password == confirm_password and new_password != "" and confirm_password != "":
        st.success("Password Confirmed")
    else:
        st.warning("Passwords not the same")

    if st.button("Submit"):
        create_usertable()
        hashed_new_password = generate_hashes(new_password)
        add_userdata(new_username,hashed_new_password)
        st.success("You have successfully created a new account")
        st.info("Login to Get Started")

elif choice == "Home":
    st.markdown(html_temp, unsafe_allow_html=True)


