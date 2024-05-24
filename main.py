from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from models import Order

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
    print(f"order: {order}")
    return templates.TemplateResponse("home.jinja", {"request": request})
