from fastapi.testclient import TestClient
from app.main import app, reformat_form_fields
from models import Order

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200

def mock_reformat_form_fields():
    return Order(q="test", cuisineType=["american"], mealType=["breakfast"], diet=["low-carb"], health=["peanut-free"])

app.dependency_overrides[reformat_form_fields] = mock_reformat_form_fields
def test_generate_meal_recipe():
    response = client.post("/")
    assert response.status_code == 200
