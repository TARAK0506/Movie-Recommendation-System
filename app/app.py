import pickle
import streamlit as st # type: ignore
import requests
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key={YOUR API KEY}&language=en-US".format(movie_id)
    
    response = requests.get(url)
    data = response.json()
    if data is None:
        print(f"Error: No data returned for movie_id {movie_id}")
        return None

    if 'poster_path' not in data:
        print(f"Error: 'poster_path' not found in data for movie_id {movie_id}")
        return None
    
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(similarity[movie_index])), reverse=True, key=lambda x: x[1])

    recommended_movie_names = []
    recommended_movie_posters = []
    for i in movies_list[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movie_names.append(movies.iloc[i[0]].title)

        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movie_names,recommended_movie_posters


st.title('Movie Recommender System')

movies_dict = pickle.load(open(r'C:\Users\tarak\Downloads\ML Projects\Movie Recommendation System\models\movies_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open(r'C:\Users\tarak\Downloads\ML Projects\Movie Recommendation System\models\similarity.pkl','rb'))

selected_movie_name = st.selectbox(
    "Select a movie from the dropdown",
    movies['title'].values
)


if st.button('Show Recommendation'):

    recommended_movie_names,recommended_movie_posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])




