import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poste(moive_id):
     responce = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8a5b5879a3c61ee2ca3e536245035b10&language=en-US'.format(moive_id))
     data = responce.json()
     poster_path = data['poster_path']
     full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
     return full_path
     #return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
#new_df = movies.copy()
def recommend(movie):
    # find the index of the selected movie
    movie_index = new_df[movies["title"] == movie].index[0]
    
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



movies_dict = pickle.load(open('movies_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

st.title("Moive Recommender System")
selected_moive_name = st.selectbox('Select the moive?',movies['title'].values)


if st.button('Recommend'):
 names ,posters = recommend(selected_movie_name)
  col1, col2, col3, col4, col5 = st.beta_columns(5)
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

 
	








