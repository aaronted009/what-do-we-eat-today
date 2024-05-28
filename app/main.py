from fastapi import FastAPI, Request, Response, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from models import Order
from dotenv import load_dotenv
import os
import requests
import logging
import random
from typing import Annotated

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


async def reformat_form_fields(request: Request):
    """Reformat submitted form fields so it could comply with API parameters type."""
    async with request.form() as form:
        q = form.get("q")
        cuisineType = form.getlist("cuisineType") if "cuisineType" in form else []
        mealType = form.getlist("mealType") if "mealType" in form else []
        diet = form.getlist("diet") if "diet" in form else []
        health = form.getlist("health") if "health" in form else []
    
    order = Order(q=q, cuisineType=cuisineType, mealType=mealType, diet=diet, health=health)
    return order


@app.post("/")
async def generate_meal_recipe(
    request: Request, order: Annotated[Order, Depends(reformat_form_fields)]
) -> Response:
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
        "type": "public",  # Type of recipes to search for.
    }
    try:
        response = requests.get(url=search_recipes_url, params=params)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        
    if response:
        recipes_data = response.json()
        # Retrieve one of the recipes randomly
        number_of_returned_recipes = len(recipes_data["hits"])  # Get the returned number of recipes
        if number_of_returned_recipes:
            random_recipe_index = random.randint(0, number_of_returned_recipes - 1)
            random_recipe = recipes_data["hits"][random_recipe_index]["recipe"]  # Get randomly one of the recipes
        else:
            random_recipe = None
    else:
        random_recipe = None
    return templates.TemplateResponse(
        "home.jinja", {"request": request, "recipe": random_recipe}
    )
