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
st.subheader("Effortlessly find recipes right at your fingertips.")
st.write("")
st.write(
    "Discover delicious recipes by inputting any ingredient. Instantly receive recipe ideas, "
    "step-by-step instructions, and nutritional information, all in one place! "
)
st.markdown("<hr>", unsafe_allow_html=True)

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
        # Meal type filter
        meal_type = st.selectbox("Select meal type", ["Any", "Breakfast", "Brunch", "Lunch", "Dinner", "Teatime"])

        # Allergen filter (e.g., exclude gluten, dairy, etc.)
        allergen_options = ["Gluten-Free", "Dairy-Free", "Peanut-Free", "Tree-Nut-Free", "Vegan", "Vegetarian"]
        selected_allergens = st.multiselect("Exclude recipes with these allergens", allergen_options)
with col2:
    st.write("")

st.markdown("<hr>", unsafe_allow_html=True)


# Handle API Requests
def load_recipes(ingredient, meal_type, selected_allergens):
    with st.spinner("Loading recipes..."):
        time.sleep(2)

    filters = ""
    if meal_type != "Any":
        filters += f"&mealType={meal_type.lower()}"
    if selected_allergens:
        health_labels = ",".join(selected_allergens).lower().replace("-", "")
        filters += f"&health={health_labels}"

    # Construct the API request URL
    url = f"{BASE_URL}{RECIPE_URL}?type=public&q={ingredient}&app_id={RECIPE_APP_ID}&app_key={RECIPE_APP_KEY}&random=true&from=0&to=20"

    # Make the GET request
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        if 'hits' in data and data['hits']:
            # Button to refresh the recipes
            refresh_button_html = """
                <style>
                div.stButton > button {
                    background-color: #fc4c4c;
                    color: white;
                    border-radius: 16px;
                    border: none;
                    padding: 8px 16px;
                    font-size: 16px;
                    font-weight: bold;
                    cursor: pointer;
                }
                div.stButton > button:hover {
                    background-color: darkred;
                }
                </style>
            """

            st.markdown(refresh_button_html, unsafe_allow_html=True)

            if st.button("Refresh Recipes", key=str(time.time())):  # Unique key generated using the current timestamp
                if ingredient_name:
                    load_recipes(ingredient_name, meal_type, selected_allergens)
                else:
                    st.warning("Please enter an ingredient first!")

            st.subheader("Results: ")
            st.info("For more details, click on the images for direct source.")
            hits = data['hits']

            images = []
            labels = []
            truncated_labels = []
            calories = []
            urls = []
            num_ingredients_list = []
            sources = []
            servings = []
            carbs = []
            fats = []
            protein = []

            for hit in hits:
                recipe = hit['recipe']
                label = recipe.get('label', 'No label available')
                image = recipe.get('image', 'No image available')
                calorie = recipe.get('calories', 'No calories available')
                url = recipe.get('url', 'No url available')
                source = recipe.get('source', 'No source available')
                serving = recipe.get('yield', 'No yield available')
                carb = recipe['totalNutrients']['CHOCDF']['quantity']
                fat = recipe['totalNutrients']['FAT']['quantity']
                protein_content = recipe['totalNutrients']['PROCNT']['quantity']


                ingredients = recipe.get('ingredients', [])
                num_ingredients = len(ingredients)

                truncated_label = label if len(label) <= 17 else label[:17] + '...'

                images.append(image)
                labels.append(label)
                truncated_labels.append(truncated_label)
                calories.append(calorie)
                urls.append(url)
                num_ingredients_list.append(num_ingredients)
                sources.append(source)
                servings.append(serving)
                carbs.append(carb)
                fats.append(fat)
                protein.append(protein_content)

            for i in range(0, len(images), 4):
                cols = st.columns(4)

                for idx, col in enumerate(cols):
                    if i + idx < len(images):
                        col.markdown(
                            f"""
                               <div style='background-color: #282434; padding: 10px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);'>
                                   <h6 style='white-space: nowrap; font-weight: bold; margin: 0;' title='{labels[i + idx]}'>{truncated_labels[i + idx]}</h6>
                                   <div style='border: 2px solid white; padding: 2px;'>
                                       <a href='{urls[i + idx]}' target='_blank'>
                                           <img src='{images[i + idx]}' title='Url: {urls[i + idx]}' style='width: 100%; height: auto;'/>
                                       </a>
                                   </div>
                                   <p style='text-align: center; font-size: 10px;'>Source: {sources[i + idx]}</p>
                                   <hr style='border: .5px solid white; margin: 2px 0;'>
                                   <p style='margin: 5px 0 0; font-size: 16px;'><span style='color: #fc4c4c;'>{round(calories[i + idx])}</span> Calories</p>
                                   <p style='margin: 5px 0 0; font-size: 15px;'><span style='color: #fc4c4c;'>{round(servings[i + idx])}</span> Servings</p>
                                   <p style='margin: 5px 0 0; font-size: 15px;'><span style='color: #fc4c4c;'>{num_ingredients_list[i + idx]}</span> Ingredients</p>
                                     <hr style='border: .5px solid white; margin: 2px 0;'>
                                   <p style='margin: 5px 0 0; font-size: 15px;'><span style='color: #fc4c4c;'>{round(carbs[i + idx])}</span>g of Carbs</p>
                                   <p style='margin: 5px 0 0; font-size: 15px;'><span style='color: #fc4c4c;'>{round(fats[i + idx], 2)}</span>g of Fats</p>
                                   <p style='margin: 5px 0 0; font-size: 15px;'><span style='color: #fc4c4c;'>{round(protein[i + idx], 2)}</span>g of Proteins</p>
                                   <hr style='border: .5px solid white; margin: 2px 0;'>
                               </div>   
                               """,
                            unsafe_allow_html=True
                        )
                        col.write("")

                st.markdown("<hr>", unsafe_allow_html=True)
                st.write("")

        else:
            st.error("No recipes found. Please write a valid input.")
    else:
        st.write(f"Failed to retrieve recipes. Status Code: {response.status_code}")


if ingredient_name:
    load_recipes(ingredient_name, meal_type, selected_allergens)
