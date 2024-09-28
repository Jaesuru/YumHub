import streamlit as st
import requests
from dotenv import load_dotenv
import os
import time

# Load environment variables
load_dotenv()
EDAMAM_APP_ID = os.getenv('EDAMAM_APP_ID')
EDAMAM_APP_KEY = os.getenv('EDAMAM_APP_KEY')
RECIPE_APP_ID = os.getenv('RECIPE_APP_ID')
RECIPE_APP_KEY = os.getenv('RECIPE_APP_KEY')

BASE_URL = 'https://api.edamam.com/'
RECIPE_URL = 'api/recipes/v2'

# Introduction
st.image("YumHub_logo.png", caption="", width=750)
st.markdown("<hr>", unsafe_allow_html=True)
st.subheader("Effortless recipes right at your fingertips.")
st.write("")
st.write(
    "Discover delicious recipes by inputting any ingredient. Instantly receive recipe ideas, "
    "step-by-step instructions, and nutritional information, all in one place! "
)
st.markdown("<hr>", unsafe_allow_html=True)

# Search Box
st.write("Please enter a single main ingredient to find related recipes.")

col1, col2 = st.columns([10, 1])

with col1:
    ingredient_name = st.text_input("Keyword:")

with col2:
    st.image("mag_glass.png", width=75)

# Handle API Requests
if ingredient_name:
    with st.spinner("Loading recipes..."):
        time.sleep(3)
    # Construct the API request URL
    url = f"{BASE_URL}{RECIPE_URL}?type=public&q={ingredient_name}&app_id={RECIPE_APP_ID}&app_key={RECIPE_APP_KEY}"

    # Make the GET request
    response = requests.get(url)
    st.write(f"Response Status Code: {response.status_code}")
