import streamlit as st
import pickle as pkl
import pandas as pd
import requests
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# Authenticate
gauth = GoogleAuth()
gauth.LocalWebserverAuth()  # Creates local web server for authentication

drive = GoogleDrive(gauth)

# Function to download a file from Google Drive using pydrive
def download_file(file_id, file_name):
    try:
        file = drive.CreateFile({'id': file_id})
        file.GetContentFile(file_name)
        print(f"File {file_name} downloaded successfully.")
    except Exception as e:
        print(f"Error downloading file: {e}")

# Download the movie list and similarity matrix files using pydrive
download_file('1sA855TxW06kVm-PISKG2zQOamy_4qmUO', 'simi.pkl')
download_file('your_movie_list_file_id', 'movie_list.pkl')  # Replace with your actual movie list file ID

# Function to fetch movie poster
def fetch_poster(movie_id):
    try:
        response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=1f5930a5b48827077a2d420afa7fa447')
        data = response.json()
        poster_url = "https://image.tmdb.org/t/p/w500" + data['poster_path']
        return poster_url
    except Exception as e:
        print(f"Error fetching poster: {e}")
        return "https://image.tmdb.org/t/p/w500/default_image.jpg"  # Placeholder image if there's an error

# Function to recommend movies
def recommend_movies(movie):
    try:
        movies_index = movies[movies['title'] == movie].index[0]
        distance = simi[movies_index]
        movies_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]  # Top 5 recommendations

        recommend_movies = []
        poster = []
        for i in movies_list:
            movie_id = movies.iloc[i[0]].movie_id
            recommend_movies.append(movies.iloc[i[0]].title)
            poster.append(fetch_poster(movie_id))
        return recommend_movies, poster
    except Exception as e:
        print(f"Error in recommending movies: {e}")
        return [], []

# Load movie list and similarity data
movies_list = pkl.load(open('movie_list.pkl', 'rb'))
movies = pd.DataFrame(movies_list)
simi = pkl.load(open('simi.pkl', 'rb'))

# Streamlit UI
st.title("Movie Recommendation System")

option = st.selectbox('Choose a Movie', movies['title'].values)
if st.button('Recommend Movie'):
    with st.spinner('Generating recommendations...'):
        name, posters = recommend_movies(option)
        if name and posters:
            col1, col2, col3, col4, col5 = st.columns(5)
            for i, col in enumerate([col1, col2, col3, col4, col5]):
                with col:
                    st.text(name[i])
                    st.image(posters[i])
        else:
            st.error("Sorry, no recommendations available.")
