import streamlit as st
import pickle as pkl
import pandas as pd
import requests
import gdown
import pickle

file_id = "1sA855TxW06kVm-PISKG2zQOamy_4qmUO"  # Replace with your actual file ID
url = f"https://drive.google.com/uc?id=1sA855TxW06kVm-PISKG2zQOamy_4qmUO"
output = "simi.pkl"

# Download the file
gdown.download(url, output, quiet=False)

# Load the similarity matrix
with open(output, "rb") as f:
    simi = pickle.load(f)


def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=1f5930a5b48827077a2d420afa7fa447'.format(movie_id))
    data = response.json()
    print(data)
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']


def recommend_movies(movie):
    movies_index = movies[movies['title'] == movie].index[0]
    distance = simi[movies_index]
    movies_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]


    recommend_movies=[]
    poster=[]
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommend_movies.append(movies.iloc[i[0]].title)
        poster.append(fetch_poster(movie_id))
    return recommend_movies, poster


movies_list = pkl.load(open('movie_list.pkl', 'rb'))
movies = pd.DataFrame(movies_list)
simi = pkl.load(open('simi.pkl', 'rb'))

st.title("Movie Recommendation System")


option = st.selectbox('Name your Movie', movies_list['title'].values)
if st.button('Recommend Movie'):
    name,posters=recommend_movies(option)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(name[0])
        st.image(posters[0])
    with col2:
        st.text(name[1])
        st.image(posters[1])
    with col3:
        st.text(name[2])
        st.image(posters[2])
    with col4:
        st.text(name[3])
        st.image(posters[3])
    with col5:
        st.text(name[4])
        st.image(posters[4])
