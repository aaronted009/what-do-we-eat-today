from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from models import Order
from dotenv import load_dotenv
import os
import requests
import logging
import random

load_dotenv()

edamam_app_id = os.getenv("EDAMAM_APP_ID")
edamam_app_key = os.getenv("EDAMAM_APP_KEY")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def home(request: Request) -> Response:
    """Home page."""
    return templates.TemplateResponse("home.jinja", {"request": request})


@app.post("/")
async def generate_meal_recipe(request: Request, order: Order) -> Response:
    """Retrieve generated meal recipe."""
    # Request to API
    search_recipes_url = "https://api.edamam.com/api/recipes/v2"
    params = {
        "q": order.q,
        "cuisineType": order.cuisineType,
        "mealType": order.mealType,
        "diet": order.diet,
        "health": order.health,
        "app_id": edamam_app_id,
        "app_key": edamam_app_key,
        "type": "public", # Type of recipes to search for.
    }
    try:
        response = requests.get(url=search_recipes_url, params=params)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    recipes_data = response.json()
    
    # Retrieve one of the recipes randomly
    number_of_returned_recipes: int = recipes_data["count"] # Get the returned number of recipes
    random_recipe_index = random.randint(0, number_of_returned_recipes) # Get randomly one of the recipes
    random_recipe = recipes_data["hits"][random_recipe_index]["recipe"]

    return templates.TemplateResponse("home.jinja", {"request": request, "recipe": random_recipe})
