import streamlit as st
import pickle
import requests

# Load movie data
movie_list = pickle.load(open('movie.pkl','rb'))
similarity_vector = pickle.load(open('sim.pkl','rb'))

# TMDB API key
API_KEY = "e39cfab59be31f8572681ea2ad0d3cc2"

# Function to fetch poster from TMDB
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    return "https://image.tmdb.org/t/p/w500" + poster_path if poster_path else None


# Function to recommend movies
def recommend_temp(movie):
    matches = movie_list[movie_list['title'].str.lower() == movie.lower()]
    if matches.empty:
        st.error(f"❌ Movie '{movie}' not found in dataset.")
        return [], [], None

    index = matches.index[0]
    movie_id = matches.iloc[0].movie_id
    selected_poster = fetch_poster(movie_id)  # Poster for selected movie

    distances = sorted(list(enumerate(similarity_vector[index])), reverse=True, key=lambda x: x[1])

    recommended_movies = []
    recommended_posters = []

    for i in distances[1:6]:
        movie_id = movie_list.iloc[i[0]].movie_id
        recommended_movies.append(movie_list.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
    
    return recommended_movies, recommended_posters, selected_poster


# Streamlit UI
st.title("🎬 Movie Recommender Web App")

movie = st.text_input("Enter your Movie Name").lower()


if st.button("search"):
    names, posters, selected_poster = recommend_temp(movie)

    if selected_poster:
        st.subheader("🎞️ Selected Movie:")
        st.image(selected_poster, caption=movie, use_container_width=True)

    if names:
        st.subheader("📽️ Recommended Movies:")
        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                st.image(posters[i], use_container_width=True)
                st.markdown(f"**{names[i]}**")

