from typing import Optional, Annotated
from fastapi import FastAPI, Request, Response, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def home(request: Request) -> Response:
    """Home page."""
    return templates.TemplateResponse("home.jinja", {"request": request})


@app.post("/")
async def generate_meal_recipe(
    request: Request,
    query: Annotated[str, Form()],
    cuisine: Annotated[Optional[str], Form()] = None,
    type: Annotated[Optional[str], Form()] = None,
    diet: Annotated[Optional[str], Form()] = None,
    intolerances: Annotated[Optional[str], Form()] = None,
) -> Response:
    """Retrieve generated meal recipe."""
    return templates.TemplateResponse("home.jinja", {"request": request})
