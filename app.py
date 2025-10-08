import streamlit as st
import pickle
import pandas as pd
import requests

# Fetch poster
def fetch_poster(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=8a5b5879a3c61ee2ca3e536245035b10&language=en-US'
    )
    data = response.json()
    poster_path = data.get('poster_path')
    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"

# Load movies and precomputed top similar movies
movies_dict = pickle.load(open('movies_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)
new_df = movies.copy()
top_similar = pickle.load(open('similarity.pkl.gz','rb'))  # precomputed top-N

def recommend(movie):
    movie_index = new_df[new_df["title"] == movie].index[0]
    similar_indices = top_similar[movie_index]

    recommended_movies = []
    recommended_posters = []

    for i in similar_indices:
        recommended_movies.append(new_df.iloc[i].title)
        recommended_posters.append(fetch_poster(new_df.iloc[i].movie_id))

    return recommended_movies, recommended_posters

# Streamlit UI
st.title("Movie Recommender System")
selected_movie_name = st.selectbox('Select the movie', movies['title'].values)

if st.button('Show Recommendation'):
    names, posters = recommend(selected_movie_name)

    # Dynamic columns for any number of recommendations
    cols = st.columns(len(names))
    for col, name, poster in zip(cols, names, posters):
        with col:
            st.text(name)
            st.image(poster)
