import streamlit as st
import os
from dotenv import load_dotenv
from services.backend_client import fetch_news
from services.background import executor


load_dotenv()

# HUN
# Beállítjuk az oldalnak a nevét, és egy icont mellé

# ENG
# We set the page name, and add an icon

st.set_page_config(
    page_title="NewsAI",
    page_icon="⛅"
)

# HUN
# azért kell nekünk, mert a streamlit minden interakció utána újra fut, ezért valahol tárolnunk kell 
# azt az információt, hogy éppen tiltva van a gomb nyomása, vagy sem.

# ENG
# We need this because Streamlit reruns after every interaction, so we need to store
# the information somewhere about whether the button is currently disabled or not.

if "loading" not in st.session_state: 
    st.session_state.loading = False

if "future" not in st.session_state:
    st.session_state.future = None

if "news_data" not in st.session_state:
    st.session_state.news_data = None

if "error" not in st.session_state:
    st.session_state.error = None


st.title("Welcome to NewsAI Service⛅")


# HUN
# Beállítjuk, hogy a form-ba legördülő menüből bírjunk választani, kötelezően kell választani

# ENG
# We'll set it up so that we can select an option from the drop-down menu in the form; a selection is required.
with st.form("my_form"):
    st.write("Inside a form")
    news_number = st.selectbox("Pick a number", 
                               range(1, 11), 
                               index=None, 
                               placeholder="Select a number")
    
    news_topic = st.selectbox("Pick a Topic", 
                              ["Law", "Economy", "War"], 
                              index=None, 
                              placeholder="Select a topic")
    
    news_language = st.selectbox("Pick a Language", 
                                 ["Hungarian", "German", "English"], 
                                 index=None, 
                                 placeholder="Select a language")
    
    submitted = st.form_submit_button("Submit", disabled=st.session_state.loading)

# HUN
# megnézzük, hogy mindent kiválaszottunk-e, ha igen akkor végre hajtja a lekérést, ha nem akkor hibát dob

# ENG
# We check to see if we've selected everything; if so, the query is executed; if not, an error is thrown
if submitted:
    if (news_number is None) or (news_topic is None) or (news_language is None):
        st.error("Please select all options.")

    else:
        st.session_state.news_data = None
        st.session_state.error = None
        
        BACKEND = os.getenv("BACKEND_URL")
        future = executor.submit(
            fetch_news, 
            f"{BACKEND}/news/latest",
                {
                    "category": news_topic,
                    "language": news_language,
                    "limit": news_number
                }
            )

        st.session_state.future = future
        st.session_state.loading = True

        st.rerun()

@st.fragment(run_every=0.5)
def check_future():
    future = st.session_state.future

    if future is None:
        return

    if future.done():
        try:
            data = future.result()

            st.session_state.loading = False
            st.session_state.future = None
            st.session_state.news_data = data

            st.rerun()

        except Exception as e:
            st.session_state.loading = False
            st.session_state.future = None
            st.session_state.error = str(e)
            st.rerun()


check_future()

if st.session_state.news_data is not None:
    st.subheader("Latest news")
    st.write(st.session_state.news_data)

if st.session_state.error is not None:
    st.write(st.session_state.error)