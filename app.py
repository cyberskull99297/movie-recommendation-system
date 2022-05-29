import streamlit as st
import pickle
import pandas as pd
import requests
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu
from PIL import Image

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

    # Use local CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("style/style.css")

img_about_me = Image.open("Images/IMG_20220127_204841.png")

lottie_coding = load_lottieurl("https://assets9.lottiefiles.com/private_files/lf30_bb9bkg1h.json")

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters

movie_list = pickle.load(open('movie_list.pkl', 'rb'))

movies = pd.DataFrame(movie_list)

similarity = pickle.load(open('similarity.pkl', 'rb'))

col1, col2, col3 = st.columns([1,6,1])

with col1:
    st.write("")

with col2:
    st_lottie(lottie_coding, height=300, key="coding")

with col3:
    st.write("")
        
    with st.sidebar:

        selected2 = option_menu(None, ["Home", "Contact Me", "---", "About Me"], 
        icons=['house', 'envelope', None, "person-fill"], 
        menu_icon="cast", default_index=0, orientation="horizontal")

        if selected2 == "Home":
            st.write("This application is a movie recommendation engine which recommends you movies, based on your choices of movies. This application will give you similar results based on your watchlist.")

        if selected2 == "Contact Me":
            # ---- CONTACT ----
            with st.container():
             st.write("---")
             st.header("Get In Touch With Me!")
             st.write("##")

            # Documention: https://formsubmit.co/ !!! CHANGE EMAIL ADDRESS !!!
            contact_form = """
            <form action="https://formsubmit.co/pradeep941462@gmail.com" method="POST">
                <input type="hidden" name="_captcha" value="false">
                <input type="text" name="name" placeholder="Your name" required>
                <input type="email" name="email" placeholder="Your email" required>
                <textarea name="message" placeholder="Your message here" required></textarea>
                <button type="submit">Send</button>
            </form>
            """
            left_column, right_column = st.columns(2)
            with left_column:
                st.markdown(contact_form, unsafe_allow_html=True)
            with right_column:
                st.empty()

        if selected2 == "About Me":
            st.image(img_about_me)
            st.header("Harshvardhan Singh")
            st.write("##")
            st.write(
            """
            Hello family!!!\n
            I am a young tech enthusiast whose vision is to bring significant changes across the globe through tech creations.
            I also have my curiosity in art and literature and also keenly interested towards books and music.
            """
        )
            st.write("[Linkedin >](https://www.linkedin.com/in/harshvardhan-singh99297/)")


st.title('Movie Recommendation System')

selected_movie_name = st.selectbox(
    'Select a movie',
    movies['title'].values)


if st.button('Recommend'):

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

   