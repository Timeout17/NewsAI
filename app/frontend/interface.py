import streamlit as st
import requests
import os
from dotenv import load_dotenv

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
        st.session_state.loading = True
        try:
            with st.spinner("Fetching news..."):
                BACKEND = os.getenv("BACKEND_URL")
                response = requests.get(
                    f"{BACKEND}/news/latest",
                    params={
                        "category": news_topic,
                        "language": news_language,
                        "limit": news_number
                    })

                data = response.json()
                st.write(data)
                
        finally:
            st.session_state.loading = False    