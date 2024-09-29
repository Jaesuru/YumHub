import streamlit as st
import requests
import openai
import time

# Your OpenAI API key (replace this with your actual key)
openai.api_key = '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'

RECIPE_APP_ID = "f9e26db3"
RECIPE_APP_KEY = "034c930d477a831055a5a94794fe1de3"
BASE_URL = 'https://api.edamam.com/'
RECIPE_URL = 'api/recipes/v2'

# Introduction
st.image("YumHub_logo.png", caption="", width=750)
st.markdown("<hr>", unsafe_allow_html=True)
st.subheader("Effortlessly find recipes right at your fingertips.")
st.write("Discover delicious recipes by inputting any ingredient. Instantly receive recipe ideas, "
         "step-by-step instructions, and nutritional information, all in one place! ")
st.markdown("<hr>", unsafe_allow_html=True)

# Sidebar Chat Box for AI Assistant
st.sidebar.title("AI Assistant")
chat_input = st.sidebar.text_input("You: ", key="chat_input")

# Initialize chat history in session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []


# Function to get AI response using the new API method
def get_ai_response(user_input):
    response = openai.completions.create(
        model="gpt-3.5-turbo-instruct",  # Use an appropriate model
        prompt=f"User: {user_input}\nAI:",
        max_tokens=150
    )
    return response['choices'][0]['text'].strip()


# Display chat interaction
if chat_input:
    st.session_state.chat_history.append(f"You: {chat_input}")
    ai_response = get_ai_response(chat_input)
    st.session_state.chat_history.append(f"AI: {ai_response}")
    st.sidebar.write(f"AI Assistant: {ai_response}")

# Display chat history
if st.session_state.chat_history:
    st.sidebar.markdown("### Chat History")
    for chat in st.session_state.chat_history:
        st.sidebar.write(chat)

# Search Box
st.write("Please enter the list of ingredients to find related recipes. (e.g., beef, egg, noodles)")
col1, col2 = st.columns([10, 1])
with col1:
    ingredient_name = st.text_input("Keyword:")
with col2:
    st.image("mag_glass.png", width=75)

col1, col2 = st.columns([10, 1])
with col1:
    with st.expander("**Optional Filters**"):
        meal_type = st.selectbox("Select meal type", ["Any", "Breakfast", "Lunch", "Dinner"])
        allergen_options = ["Gluten-Free", "Dairy-Free", "Peanut-Free", "Tree-Nut-Free", "Vegan", "Vegetarian"]
        selected_allergens = st.multiselect("Exclude recipes with these allergens", allergen_options)

st.markdown("<hr>", unsafe_allow_html=True)


# Handle API Requests for recipes
def load_recipes(ingredient, meal_type, selected_allergens, from_, to_):
    with st.spinner("Loading recipes..."):
        time.sleep(2)
    filters = ""
    if meal_type != "Any":
        filters += f"&mealType={meal_type.lower()}"
    if selected_allergens:
        health_labels = ",".join(selected_allergens).lower().replace("-", "")
        filters += f"&health={health_labels}"

    url = f"{BASE_URL}{RECIPE_URL}?type=public&q={ingredient}{filters}&app_id={RECIPE_APP_ID}&app_key={RECIPE_APP_KEY}&from={from_}&to={to_}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if 'hits' in data and data['hits']:
            display_from = from_ + 1
            display_to = min(to_, data['count'])
            st.subheader(f"Displaying: {display_from} - {display_to} recipes (out of {data['count']})")
            hits = data['hits']

            for hit in hits:
                recipe = hit['recipe']
                st.write(f"**{recipe['label']}** - {recipe['calories']} calories")
        else:
            st.error("No recipes found.")
    else:
        st.write(f"Failed to retrieve recipes. Status Code: {response.status_code}")


if ingredient_name:
    load_recipes(ingredient_name, meal_type, selected_allergens, st.session_state.get('from_', 0),
                 st.session_state.get('to_', 20))

