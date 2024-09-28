import streamlit as st
import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
EDAMAM_APP_ID = os.getenv('EDAMAM_APP_ID')
EDAMAM_APP_KEY = os.getenv('EDAMAM_APP_KEY')
RECIPE_APP_ID = os.getenv('RECIPE_APP_ID')
RECIPE_APP_KEY = os.getenv('RECIPE_APP_KEY')

BASE_URL ='api.edamam.com/'

st.markdown("""
    <style>
    .main {
        background-color: white;
        color: black;
    }
    body {
        color: black;
    }
    hr {
        border: 1px solid black; /* Enables the border */
        height: 0;  /* Ensures the height of the <hr> itself is 0, showing only the border */
    }
    h2, h3 {  /* Targets subheaders */
        color: black;  /* Makes subheader text black */
    }
    </style>
    """, unsafe_allow_html=True)

st.image("YumHub_logo.png", caption="", width=750)
st.markdown("<hr>", unsafe_allow_html=True)
st.subheader("Effortless recipes right at your fingertips.")
st.write("")
st.write("Discover delicious recipes by inputting any ingredient. Instantly receive recipe ideas, step-by-step instructions, and nutritional information, all in one place! ")
