import streamlit as st
import pickle
import pandas as pd
import requests

st.set_page_config(layout="wide", page_title="Movie Recommender")

# Load data
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_list = movies['title'].values

# --- TMDb API KEY ---
API_KEY = 'a19ee3fcfbe75a92e07782fbf236966d'

# --- Fetch poster from TMDb ---
def fetch_poster(movie_title):
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_title}"
    try:
        response = requests.get(search_url)
        data = response.json()

        for result in data.get("results", []):
            if result.get("poster_path"):
                return "https://image.tmdb.org/t/p/w500" + result["poster_path"]
        return "https://via.placeholder.com/500x750?text=No+Image"
    except:
        return "https://via.placeholder.com/500x750?text=Error"

# --- Recommend movies ---
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = [] 
    recommended_posters = []
    for i in distances[1:6]:
        title = movies.iloc[i[0]].title
        recommended_movies.append(title)
        recommended_posters.append(fetch_poster(title))
    return recommended_movies, recommended_posters

# --- Streamlit UI ---
st.markdown("<h1 style='text-align: center;'>🎬 Movie Recommender System</h1>", unsafe_allow_html=True)
selected_movie_name = st.selectbox("Select a movie to get recommendations:", movie_list)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.image(posters[i])
            st.caption(names[i])
