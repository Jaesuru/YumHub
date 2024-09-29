import streamlit as st
import requests
import time

RECIPE_APP_ID = "f9e26db3"
RECIPE_APP_KEY = "034c930d477a831055a5a94794fe1de3"

BASE_URL = 'https://api.edamam.com/'
RECIPE_URL = 'api/recipes/v2'

# Introduction
st.image("YumHub_logo.png", caption="", width=750)
st.markdown("<hr>", unsafe_allow_html=True)
st.subheader("Effortless recipes right at your fingertips.")
st.write("Discover delicious recipes by inputting any ingredient and applying filters for meal type and allergens.")
st.markdown("<hr>", unsafe_allow_html=True)

# Search Box
st.write("Please enter the list of ingredients to find related recipes. (e.g., beef, egg, noodles)")
col1, col2 = st.columns([10, 1])
with col1:
    ingredient_name = st.text_input("Keyword:")
with col2:
    st.image("mag_glass.png", width=75)

# Filters
st.write("**Optional Filters:**")

# Meal type filter
meal_type = st.selectbox("Select meal type", ["Any", "Breakfast", "Lunch", "Dinner"])

# Allergen filter (e.g., exclude gluten, dairy, etc.)
allergen_options = ["Gluten-Free", "Dairy-Free", "Peanut-Free", "Tree-Nut-Free", "Vegan", "Vegetarian"]
selected_allergens = st.multiselect("Exclude recipes with these allergens", allergen_options)

st.markdown("<hr>", unsafe_allow_html=True)

# Initialize session state for pagination
if 'page' not in st.session_state:
    st.session_state.page = 1
    st.session_state.from_ = 0
    st.session_state.to = 20
    st.session_state.next_link = None  # Initialize the next link

# Handle API Requests
def load_recipes(ingredient, meal_type, selected_allergens, from_, to_):
    with st.spinner("Loading recipes..."):
        time.sleep(2)

    filters = ""
    if meal_type != "Any":
        filters += f"&mealType={meal_type.lower()}"
    if selected_allergens:
        health_labels = ",".join(selected_allergens).lower().replace("-", "")
        filters += f"&health={health_labels}"

    # Use the next link if it exists; otherwise construct a new URL
    if st.session_state.next_link:
        url = st.session_state.next_link
    else:
        url = f"{BASE_URL}{RECIPE_URL}?type=public&q={ingredient}{filters}&app_id={RECIPE_APP_ID}&app_key={RECIPE_APP_KEY}&from={from_}&to={to_}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'hits' in data and data['hits']:
            # Correct the range displayed
            display_from = from_ + 1
            display_to = min(to_, data['count'])

            st.subheader(f"Displaying {display_from} - {display_to} recipes (out of {data['count']})")
            hits = data['hits']
            images, labels, calories, urls, num_ingredients_list, sources, total_weights = [], [], [], [], [], [], []

            for hit in hits:
                recipe = hit['recipe']
                label = recipe.get('label', 'No label available')
                image = recipe.get('image', 'No image available')
                calorie = recipe.get('calories', 'No calories available')
                url = recipe.get('url', 'No url available')
                source = recipe.get('source', 'No source available')
                total_weight = recipe.get('totalWeight', 'N/A')

                ingredients = recipe.get('ingredients', [])
                num_ingredients = len(ingredients)

                truncated_label = label if len(label) <= 17 else label[:17] + '...'

                images.append(image)
                labels.append(truncated_label)
                calories.append(calorie)
                urls.append(url)
                num_ingredients_list.append(num_ingredients)
                sources.append(source)
                total_weights.append(total_weight)

            for i in range(0, len(images), 4):
                cols = st.columns(4)
                for idx, col in enumerate(cols):
                    if i + idx < len(images):
                        col.markdown(
                            f"""
                            <div style='background-color: #282434; padding: 10px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);'>
                                <h6 style='white-space: nowrap; font-weight: bold; margin: 0;'>{labels[i + idx]}</h6>
                                <div style='border: 2px solid white; padding: 2px;'>
                                    <img src='{images[i + idx]}' title='Url: {urls[i + idx]}' style='width: 100%; height: auto;'/>
                                </div>
                                <p style='text-align: center; font-size: 10px;'>Source: {sources[i + idx]}</p>
                                <p style='margin: 5px 0 0; font-size: 16px;'><span style='color: #fc4c4c;'>{round(total_weights[i + idx], 2)}</span> Grams</p>
                                <p style='margin: 5px 0 0; font-size: 16px;'><span style='color: #fc4c4c;'>{round(calories[i + idx])}</span> Calories</p>
                                <p style='margin: 5px 0 0; font-size: 14px;'><span style='color: #fc4c4c;'>{num_ingredients_list[i + idx]}</span> Ingredients</p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

            # Check for next link
            if "_links" in data and "next" in data["_links"]:
                st.session_state.next_link = data["_links"]["next"]["href"]
            else:
                st.session_state.next_link = None  # Reset if no next link

            # Navigation buttons
            st.markdown("<hr>", unsafe_allow_html=True)
            if st.session_state.page > 1:
                if st.button("Back"):
                    st.session_state.page -= 1
                    st.session_state.from_ -= 20
                    st.session_state.to -= 20
                    st.session_state.next_link = None  # Reset next link on back
                    st.rerun()  # Refresh to show new results
            if st.session_state.next_link:
                if st.button("Next"):
                    st.session_state.page += 1
                    st.session_state.from_ += 20
                    st.session_state.to += 20
                    st.rerun()  # Refresh to show new results
        else:
            st.error("No recipes found. Please write a valid input.")
    else:
        st.write(f"Failed to retrieve recipes. Status Code: {response.status_code}")

if ingredient_name:
    load_recipes(ingredient_name, meal_type, selected_allergens, st.session_state.from_, st.session_state.to)
