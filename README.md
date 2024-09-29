# Recipe Finder Application

![YumHub Logo](YumHub_logo.png)

## Overview

The Recipe Finder application allows users to effortlessly discover delicious recipes based on their chosen ingredients. Users can input any ingredient, and the application provides a variety of recipes instantly.

## Features

- **Ingredient Search**: Input any ingredient to find related recipes.
- **Optional Filters**: Users can filter recipes based on meal type and allergens.
- **Recipe Display**: View recipes along with images, calories, servings, and ingredient count.
- **Quick Access to Sources**: Click on recipe images to navigate directly to the source website for more details.

## Technologies Used

- **Python**: The programming language used to build the application.
- **Streamlit**: A framework for building interactive web applications in Python.
- **Requests**: A library for making HTTP requests to fetch recipe data from an API.
- **dotenv**: A module to load environment variables from a `.env` file.
- **Edamam API**: An API used to fetch recipe data based on user input.

## Installation

1. **Clone the Repository**:
- bash
- Copy code
- git clone <repository-url>
- cd <repository-directory>
2. **Set Up Environment Variables:** Create a .env file in the root directory of the project with the following content:
EDAMAM_APP_ID=<your-edamam-app-id>
EDAMAM_APP_KEY=<your-edamam-app-key>
RECIPE_APP_ID=<your-recipe-app-id>
RECIPE_APP_KEY=<your-recipe-app-key>
3. **Install Required Packages:**
- bash
- Copy code
- pip install -r requirements.txt
## Usage
- Run the application:

- bash
- Copy code
- streamlit run app.py
- Open your browser and go to http://localhost:8501 to view the application.

- Enter your desired ingredients into the search box and optionally select filters for meal type and allergens.

- Click on the recipe images to view the full recipe on the source website.
