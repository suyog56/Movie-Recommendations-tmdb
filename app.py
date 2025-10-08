import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=8a5b5879a3c61ee2ca3e536245035b10&language=en-US'.format(movie_id)
    )
    data = response.json()
    poster_path = data.get('poster_path')
    if poster_path:
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"

# Load movie data
movies_dict = pickle.load(open('movies_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)
new_df = movies.copy()  # Fix missing new_df

# Dummy similarity matrix (replace with your actual similarity)
#similarity = pickle.load(open('similarity.pkl','rb'))  # assuming you have this

def recommend(movie):
    # find the index of the selected movie
    movie_index = new_df[new_df["title"] == movie].index[0]
    
    # compute similarity scores
    distances = similarity[movie_index]
    
    # get top 5 similar movies (excluding the first itself)
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    recommended_posters = []
    
    for i in movie_list:
        movie_id = new_df.iloc[i[0]].movie_id
        recommended_movies.append(new_df.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
    
    return recommended_movies, recommended_posters

# Streamlit UI
st.title("Movie Recommender System")
selected_movie_name = st.selectbox('Select the movie', movies['title'].values)

if st.button('Show Recommendation'):
    names, posters = recommend(selected_movie_name)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])

